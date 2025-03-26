"""Configuración de Gunicorn para producción"""

# Número de workers (procesos)
# Se recomienda (2 x núcleos) + 1
workers = 4

# Número de hilos por worker
threads = 2

# Tiempo de espera antes de matar un worker que no responde
timeout = 60

# Dirección y puerto donde escuchar
bind = "0.0.0.0:8505"

# Configuración de logs
accesslog = "-"  # Enviar a stdout
errorlog = "-"   # Enviar a stderr
loglevel = "info"

# Recargar automáticamente cuando cambia el código (solo para desarrollo)
# reload = True
