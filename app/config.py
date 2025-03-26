import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """Clase de configuración para la aplicación Flask"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-predeterminada'
    WINDOWS_API = os.environ.get('WINDOWS_API')
    WINDOWS_API_POST = os.environ.get('WINDOWS_API_POST')
    
    # Configuración para la base de datos FP
    DB_CONFIG_FP = {
        'usuario': os.environ.get('DB_USER_FP'),
        'contrasena': os.environ.get('DB_PASSWORD_FP'),
        'servidor': os.environ.get('DB_SERVER_FP'),
        'baseDatos': os.environ.get('DB_DATABASE_FP'),
        'parametros': [],
        'esValido': True,
        'mensaje': '',
        'query': '',
        'tipo': '',
        'parametrosSalida': '',
        'resultado': ''
    }
    
    # Configuración para la base de datos E
    DB_CONFIG_E = {
        'usuario': os.environ.get('DB_USER_E'),
        'contrasena': os.environ.get('DB_PASSWORD_E'),
        'servidor': os.environ.get('DB_SERVER_E'),
        'baseDatos': os.environ.get('DB_DATABASE_E'),
        'parametros': [],
        'esValido': True,
        'mensaje': '',
        'query': '',
        'tipo': '',
        'parametrosSalida': '',
        'resultado': ''
    }
    
    # Configuración para la base de datos AHI
    DB_CONFIG_AHI = {
        'usuario': os.environ.get('DB_USER_AHI'),
        'contrasena': os.environ.get('DB_PASSWORD_AHI'),
        'servidor': os.environ.get('DB_SERVER_AHI'),
        'baseDatos': os.environ.get('DB_DATABASE_AHI'),
        'parametros': [],
        'esValido': True,
        'mensaje': '',
        'query': '',
        'tipo': '',
        'parametrosSalida': '',
        'resultado': ''
    }
