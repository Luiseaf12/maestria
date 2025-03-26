# Guía de Despliegue con Docker Compose

## Preparación

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
   - [Instalar Docker](https://docs.docker.com/get-docker/)
   - [Instalar Docker Compose](https://docs.docker.com/compose/install/)

2. Verifica que tu archivo `.env` contenga todas las variables de entorno necesarias.

## Despliegue en Desarrollo

Para ejecutar la aplicación en modo desarrollo:

```bash
docker-compose up
```

Esto construirá la imagen Docker y ejecutará el contenedor. La aplicación estará disponible en `http://localhost:8000`.

Para ejecutar en segundo plano:

```bash
docker-compose up -d
```

Para detener los contenedores:

```bash
docker-compose down
```

## Despliegue en Producción

Para un entorno de producción, considera estos ajustes adicionales:

1. Modifica el archivo `gunicorn_config.py` según tus necesidades:
   - Ajusta el número de workers según los recursos del servidor
   - Configura los logs adecuadamente

2. Considera añadir un servidor proxy inverso como Nginx:
   - Para manejar SSL/TLS
   - Para servir archivos estáticos
   - Para balanceo de carga

3. Configura volúmenes persistentes para datos importantes.

## Explicación sobre el Servidor de Desarrollo vs Producción

### ¿Qué significa la advertencia?

La advertencia que ves al ejecutar `python run.py`:

```
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
```

Indica que el servidor web integrado de Flask está diseñado solo para desarrollo y no para producción debido a:

1. **Rendimiento**: No está optimizado para manejar múltiples solicitudes simultáneas.
2. **Seguridad**: No incluye características de seguridad necesarias para entornos de producción.
3. **Estabilidad**: No está diseñado para ejecutarse por largos períodos.

### Solución para Producción

En esta configuración Docker, usamos Gunicorn como servidor WSGI de producción, que:

1. **Maneja múltiples procesos** (workers) para atender solicitudes simultáneas.
2. **Es más estable y seguro** para entornos de producción.
3. **Tiene mejor rendimiento** bajo carga.

Cuando ejecutas la aplicación con Docker Compose, se usa Gunicorn automáticamente gracias a la configuración en el Dockerfile.

## Comandos Útiles

### Ver logs de los contenedores
```bash
docker-compose logs -f
```

### Reconstruir la imagen después de cambios
```bash
docker-compose build
```

### Ejecutar comandos dentro del contenedor
```bash
docker-compose exec ml-service python -c "import flask; print(flask.__version__)"
```
