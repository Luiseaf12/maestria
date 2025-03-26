FROM python:3.9-slim

WORKDIR /app

# Copiar los archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto que usa la aplicación
EXPOSE 8505

# Comando para ejecutar la aplicación con gunicorn
CMD ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]

# Comando para ejecutar la aplicación con gunicorn directamente con parámetros, no utiliza el archivo gunicorn_config.py
#CMD ["gunicorn", "--bind", "0.0.0.0:8505", "--workers", "4", "--threads", "2", "--timeout", "60", "wsgi:app"]