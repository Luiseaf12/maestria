from flask import render_template, request, redirect, url_for
from app.main import bp
from app.services.api_service import get_plan_produccion_por_producto_data, get_plan_produccion_por_articulo_data, get_existencias_articulo_data, get_existencias_articulo_data_tipo_procedimiento
from app.utils.data_service import transform_plan_produccion_por_producto_data, transform_plan_produccion_por_articulo_data
import pandas as pd


@bp.route('/indice1')
def indice1():
    """Ruta principal que muestra el calendario de producción"""
    # Obtener datos de la API
    data = get_plan_produccion_por_producto_data()

    # Obtener parámetros de ordenamiento
    sort_by = request.args.get('sort_by', 'INDICE_PRIORIDAD_ACTUAL')
    sort_order = request.args.get('sort_order', 'desc')

    # Obtener la línea de producción seleccionada del parámetro de consulta
    linea_produccion_seleccionada = request.args.get('linea_produccion', '')

    # Transformar los datos usando el servicio
    transformed_data = transform_plan_produccion_por_producto_data(
        data,
        sort_by=sort_by,
        sort_order=sort_order,
        linea_produccion_seleccionada=linea_produccion_seleccionada
    )

    return render_template("indice1.html",
                           calendario=transformed_data['calendario_produccion'],
                           lineas_produccion=transformed_data['lineas_produccion'],
                           linea_seleccionada=linea_produccion_seleccionada,
                           sort_by=sort_by,
                           sort_order=sort_order)


@bp.route('/')
def index():
    # Sirve para redireccionar
    # return redirect(url_for('main.indice1'))

    # Obtener datos de la API
    data = get_plan_produccion_por_articulo_data()

    # print(data)

    # Obtener parámetros de ordenamiento
    sort_by = request.args.get('sort_by', 'INDICE')
    sort_order = request.args.get('sort_order', 'desc')

    # Obtener la línea de producción seleccionada del parámetro de consulta
    linea_produccion_seleccionada = request.args.get('linea_produccion', '')

    # Transformar los datos usando el servicio
    transformed_data = transform_plan_produccion_por_articulo_data(
        data,
        sort_by=sort_by,
        sort_order=sort_order,
        linea_produccion_seleccionada=linea_produccion_seleccionada
    )
    # print(transformed_data)

    return render_template("PlanificacionProduccion.html",
                           data=transformed_data['data'],
                           lineas_produccion=transformed_data['lineas_produccion'],
                           linea_seleccionada=linea_produccion_seleccionada,
                           sort_by=sort_by,
                           sort_order=sort_order
                           )


@bp.route('/existencias_articulo', methods=['GET'])
def existencias_articulo():
    # Obtener parámetros de la URL
    cod_art = request.args.get('COD_ART', '')
    tipo = request.args.get('TIPO', 'TODAS')
    articulo = request.args.get('ARTICULO', '')

    # Obtener parámetros de ordenamiento
    sort_by = request.args.get('sort_by', 'NOM_ALM')
    sort_order = request.args.get('sort_order', 'asc')

    # Obtener datos de la API
    data = get_existencias_articulo_data(
        COD_ART=cod_art, TIPO=tipo)

    # Convertir a DataFrame para ordenar
    if data:
        import pandas as pd
        df = pd.DataFrame(data)

        # Mapeo de nombres de columnas en la tabla a nombres de columnas en el DataFrame
        column_mapping = {
            'Almacén': 'NOM_ALM',
            'Existencia': 'EXISTENCIA',
            'Fecha Lote Antiguo': 'FECHA_LOTE_MAS_ANTIGUO'
        }

        # Convertir el nombre de la columna de la tabla al nombre de la columna en el DataFrame
        sort_column = column_mapping.get(sort_by, sort_by)

        # Determinar si el orden es ascendente o descendente
        ascending = sort_order != 'desc'

        # Ordenar el DataFrame
        if sort_column in df.columns:
            df = df.sort_values(by=sort_column, ascending=ascending)

        # Convertir de nuevo a lista de diccionarios
        data = df.to_dict('records')

    return render_template("existencias_articulo.html",
                           data=data,
                           cod_art=cod_art,
                           ARTICULO=articulo,
                           sort_by=sort_by,
                           sort_order=sort_order)
