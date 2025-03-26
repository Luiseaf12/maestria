# Aplicación de Calendario de Producción

Esta aplicación muestra un calendario de producción basado en datos obtenidos de una API externa.

## Estructura del Proyecto

```
ml/
├── app/                    # Paquete principal de la aplicación
│   ├── api/                # Módulo para endpoints de API
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main/               # Módulo para rutas principales
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/             # Modelos de datos
│   │   └── __init__.py
│   ├── services/           # Servicios para lógica de negocio
│   │   ├── __init__.py
│   │   └── api_service.py
│   ├── static/             # Archivos estáticos
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   ├── templates/          # Plantillas HTML
│   │   └── index.html
│   ├── utils/              # Utilidades
│   │   └── __init__.py
│   ├── __init__.py         # Inicializador de la aplicación
│   └── config.py           # Configuración de la aplicación
├── .env                    # Variables de entorno (no incluido en el repositorio)
├── requirements.txt        # Dependencias del proyecto
├── run.py                  # Punto de entrada para ejecutar la aplicación
└── README.md               # Documentación del proyecto
```

## Instalación

1. Clona el repositorio
2. Crea un entorno virtual: `python -m venv venv`
3. Activa el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instala las dependencias: `pip install -r requirements.txt`
5. Crea un archivo `.env` con las variables de entorno necesarias

## Ejecución

Para ejecutar la aplicación:

```
python run.py
```

La aplicación estará disponible en `http://localhost:8000`
# maestria
