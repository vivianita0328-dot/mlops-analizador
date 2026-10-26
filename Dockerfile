# Imagen base de Python ligera
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar primero las dependencias para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto (incluyendo el JSON y main.py)
COPY . .

# --- INICIO DEL BASTIONADO (Mínimo Privilegio) ---
# Crear un usuario genérico de sistema ('appuser')
RUN useradd -m appuser
# Dar propiedad de los archivos de la app a este nuevo usuario
RUN chown -R appuser:appuser /app
# Cambiar la ejecución a 'appuser' (dejando de ser root)
USER appuser
# --- FIN DEL BASTIONADO ---

# Puerto utilizado por la API
EXPOSE 8000

# Ejecutar la aplicación FastAPI
CMD ["uvicorn", "main_2:app", "--host", "0.0.0.0", "--port", "8000"]