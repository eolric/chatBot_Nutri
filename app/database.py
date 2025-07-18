import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database_if_not_exists():
    conn = None  # Inicializa conn aquí para evitar UnboundLocalError
    try:
        # Conexión inicial sin especificar la base de datos
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "")  # Asegúrate que coincide con tu MySQL
        )
        cursor = conn.cursor()

        # Verificar si la base de datos existe, si no, crearla
        db_name = os.getenv('DB_NAME', 'nutribot_db')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✅ Base de datos '{db_name}' verificada/creada.")

        # Crear tabla si no existe
        cursor.execute(f"USE {db_name}")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                contenido TEXT NOT NULL,
                respuesta TEXT,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'mensajes' verificada/creada.")

    except Error as e:
        print(f"❌ Error de MySQL: {e}")
        raise  # Relanza el error para que FastAPI lo detecte
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "nutribot_db")
        )
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        raise