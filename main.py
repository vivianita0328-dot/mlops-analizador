import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google import genai
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
load_dotenv()

# Inicializar la aplicación
app = FastAPI(
    title="Inference API",
    description="API REST para servir un modelo de Inteligencia Artificial.",
    version="1.0.0"
)
# Inicializar el modelo

# En un escenario clásico de Machine Learning aquí podría cargarse un modelo .pkl:
# import joblib
# modelo = joblib.load("modelo.pkl")

# En este ejemplo utilizamos un LLM de Gemini.

modelo = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Modelo de entrada
class InferenceRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="Texto de entrada para realizar la inferencia."
    )


@app.post("/inferencia")
async def inferencia(request: InferenceRequest):
    try:
        respuesta = modelo.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=request.prompt,
        )
        return {
            "status": "success",
            "response": respuesta.text
        }

    except Exception as e:
        print(f"Error en la inferencia: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al realizar la inferencia"
        )


@app.get("/")
async def health_check():
    return {"status": "ok", "message": "API de inferencia funcionando correctamente"}


#dockerfile
# # Imagen base de Python
# FROM python:3.11-slim

# # Directorio de trabajo dentro del contenedor
# WORKDIR /app

# # Copiar primero las dependencias para aprovechar la caché de Docker
# COPY requirements.txt .

# # Instalar las dependencias del proyecto
# RUN pip install --no-cache-dir -r requirements.txt

# # Copiar el resto del proyecto
# COPY . .

# # Puerto utilizado por la API
# EXPOSE 8000

# # Ejecutar la aplicación FastAPI
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]