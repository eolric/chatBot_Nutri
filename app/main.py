from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
from app.database import create_database_if_not_exists, get_db_connection
from app.utils import get_gemini_response
import os
from dotenv import load_dotenv


# Carga variables de entorno
load_dotenv()

# Asegurar que la base de datos y tabla existan al iniciar
create_database_if_not_exists()

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Ruta principal (interfaz de chat)
@app.get("/", response_class=HTMLResponse)
async def chat_interface(request: Request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT contenido, respuesta 
        FROM mensajes 
        ORDER BY creado_en DESC 
        LIMIT 5
    """)
    mensajes = cursor.fetchall()[::-1]  # Invierte para mostrar los más recientes al final
    cursor.close()
    conn.close()
    
    # ¡Depuración! Esto aparecerá en la consola donde ejecutas FastAPI.
    print("Mensajes recuperados de la DB:", mensajes)
    
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "mensajes": mensajes  # Asegúrate de que esto coincide con la plantilla
    })

# Ruta para procesar mensajes
@app.post("/chat")
async def handle_chat(request: Request, user_message: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Guardar mensaje en MySQL
    cursor.execute("INSERT INTO mensajes (contenido) VALUES (%s)", (user_message,))
    conn.commit()
    message_id = cursor.lastrowid

    # 2. Obtener respuesta (simulada o de DeepSeek)
    respuesta_ia = get_gemini_response(user_message)

    # 3. Guardar respuesta en MySQL
    cursor.execute("UPDATE mensajes SET respuesta = %s WHERE id = %s", (respuesta_ia, message_id))
    conn.commit()

    # 4. Obtener TODOS los mensajes para mostrar el historial
    cursor.execute("""
        SELECT contenido, respuesta 
        FROM mensajes 
        ORDER BY creado_en DESC 
        LIMIT 5
    """)
    mensajes = cursor.fetchall()[::-1]  # Invierte para mostrar los más recientes al final
    cursor.close()
    conn.close()

    # Renderiza la plantilla con todos los mensajes
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "mensajes": mensajes  # Pasa los mensajes a la plantilla
    })