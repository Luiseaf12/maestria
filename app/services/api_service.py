import json
import time
import requests
from flask import current_app


def get_production_data_api_nsa_back():
    """Obtiene datos de producción de la API local (método alternativo)"""
    try:
        inicio = time.time()

        # Esta api esta en el nsa-back
        response = requests.get(
            'http://192.168.20.12:5000/api/reporte-produccion-plan-produccion-diario')
        # 'http://localhost:5000/api/reporte-produccion-plan-produccion-diario')

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                fin = time.time()
                tiempo_total = fin - inicio
                print(f"\nTiempo de ejecución: {tiempo_total:.2f} segundos")
                return data['data']
        return []
    except Exception as e:
        print(f"Error al obtener datos de la API: {str(e)}")
        return []


def get_plan_produccion_por_producto_data():
    """Obtiene datos de producción de la API externa"""
    try:
        # Parámetros de la consulta
        query = "MP_RPT_ML_PLAN_PRODUCCION_POR_PRODUCTO"

        # Crear el cuerpo de la solicitud usando la configuración
        body_FP = current_app.config['DB_CONFIG_FP'].copy()
        body_FP['query'] = query
        body_FP['tipo'] = "query"

        # Hacer la consulta a la API
        api_url = current_app.config['WINDOWS_API']
        response = requests.get(api_url, json=body_FP)

        # Obtener la respuesta JSON
        response_data = response.json()

        # Extraer el resultado que viene como string JSON y convertirlo a objeto Python
        resultado_str = response_data['data']['resultado']
        resultado = json.loads(resultado_str)

        # print("resultado", resultado)

        if response.status_code == 200:
            return resultado
        return []
    except Exception as e:
        print(f"Error al obtener datos de la API: {str(e)}")
        return []


def get_plan_produccion_por_articulo_data():
    """Obtiene datos de producción de la API externa"""
    try:
        # Parámetros de la consulta
        query = "MP_RPT_ML_PLAN_PRODUCCION_POR_ARTICULO"

        # Crear el cuerpo de la solicitud usando la configuración
        body_FP = current_app.config['DB_CONFIG_FP'].copy()
        body_FP['query'] = query
        body_FP['tipo'] = "query"

        # Hacer la consulta a la API
        api_url = current_app.config['WINDOWS_API']
        response = requests.get(api_url, json=body_FP)

        # Obtener la respuesta JSON
        response_data = response.json()

        # Extraer el resultado que viene como string JSON y convertirlo a objeto Python
        resultado_str = response_data['data']['resultado']
        resultado = json.loads(resultado_str)

        # print("resultado", resultado)

        if response.status_code == 200:
            return resultado
        return []
    except Exception as e:
        print(f"Error al obtener datos de la API: {str(e)}")
        return []


def get_existencias_articulo_data_tipo_procedimiento(COD_ART='', TIPO=''):
    """Obtiene datos de existencias de la API externa"""
    try:
        # Parámetros de la consulta
        query = f"MP_RPT_ML_EXISTENCIAS_ARTICULO"

        # Crear el cuerpo de la solicitud usando la configuración
        body_FP = current_app.config['DB_CONFIG_FP'].copy()
        body_FP['query'] = query
        body_FP['tipo'] = "procedimientoAlmacenado"

        body_FP['parametros'] = [
            {
                "parametro": "@COD_ART",
                "valor": str(COD_ART),
                "tipo": "string",
                "direccion": "entrada"
            },
            {
                "parametro": "@TIPO",
                "valor": str(TIPO),
                "tipo": "string",
                "direccion": "entrada"
            }
        ]

        # print("body_FP", body_FP)

        # Hacer la consulta a la API
        api_url = current_app.config['WINDOWS_API']
        response = requests.get(api_url, json=body_FP)

        # Obtener la respuesta JSON
        response_data = response.json()

        # Extraer el resultado que viene como string JSON y convertirlo a objeto Python
        resultado_str = response_data['data']['resultado']
        resultado = json.loads(resultado_str)

        # print("resultado", resultado)

        if response.status_code == 200:
            return resultado
        return []
    except Exception as e:
        print(f"Error al obtener datos de la API: {str(e)}")
        return []


def get_existencias_articulo_data(COD_ART='', TIPO=''):
    """Obtiene datos de existencias de la API externa"""
    try:
        # Parámetros de la consulta
        query = f"EXEC dbo.MP_RPT_ML_EXISTENCIAS_ARTICULO @COD_ART='{COD_ART}',@TIPO='{TIPO}'"

        # Crear el cuerpo de la solicitud usando la configuración
        body_FP = current_app.config['DB_CONFIG_FP'].copy()
        body_FP['query'] = query
        body_FP['tipo'] = "query"

        # Hacer la consulta a la API
        api_url = current_app.config['WINDOWS_API']
        response = requests.get(api_url, json=body_FP)

        # Obtener la respuesta JSON
        response_data = response.json()

        # Extraer el resultado que viene como string JSON y convertirlo a objeto Python
        resultado_str = response_data['data']['resultado']
        resultado = json.loads(resultado_str)

        # print("resultado", resultado)

        if response.status_code == 200:
            return resultado
        return []
    except Exception as e:
        print(f"Error al obtener datos de la API: {str(e)}")
        return []
