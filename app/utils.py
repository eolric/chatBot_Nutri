import os
from dotenv import load_dotenv
import google.generativeai as genai  # Importa así, no desde 'google'

load_dotenv()

def get_gemini_response(prompt: str) -> str:
    try:
        # 1. Configuración (usa la variable GEMINI_API_KEY de .env)
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # 2. Crea el modelo
        model = genai.GenerativeModel('gemini-1.5-flash')  # Modelo rápido y actual
        
        # 3. Genera la respuesta
        response = model.generate_content(
            f"""Eres NutriBot, nutricionista experto. 
            Responde de forma clara y profesional en menos de 100 palabras:
            {prompt}""",
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 500
            }
        )
        
        return response.text
        
    except Exception as e:
        print(f"❌ Error en Gemini API: {e}")
        return "Disculpa, no puedo responder ahora. Intenta más tarde."