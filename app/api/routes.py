from flask import jsonify
from app.api import bp
from app.services.api_service import get_plan_produccion_por_producto_data, get_plan_produccion_por_articulo_data

# http://127.0.0.1:8505/api/plan-produccion-por-producto


@bp.route('/plan-produccion-por-producto')
def reporte_produccion_por_producto():
    """Endpoint de API para obtener los datos de producción"""
    try:
        data = get_plan_produccion_por_producto_data()
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@bp.route('/plan-produccion-por-articulo')
def reporte_produccion_por_articulo():
    """Endpoint de API para obtener los datos de producción"""
    try:
        data = get_plan_produccion_por_articulo_data()
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
