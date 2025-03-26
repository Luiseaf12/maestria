# app/services/data_service.py
import datetime
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def transform_plan_produccion_por_producto_data(data, sort_by='INDICE_PRIORIDAD_ACTUAL', sort_order='desc', linea_produccion_seleccionada=''):
    """
    Transforma los datos de producción aplicando cálculos y filtros

    Args:
        data: Datos obtenidos de la API
        sort_by: Columna por la que ordenar los datos
        sort_order: Orden de clasificación ('asc' o 'desc')
        linea_produccion_seleccionada: Línea de producción para filtrar

    Returns:
        Diccionario con los datos transformados y metadatos
    """
    # Convertir a DataFrame
    df = pd.DataFrame(data)

    # Calcular el índice de prioridad
    df["INDICE_PRIORIDAD_ANUAL"] = df.apply(
        lambda row: row["UTILIDAD_TOTAL"] if row["EXISTENCIAS_CULIACAN"] == 0
        else (row["CANTIDAD_ULTIMO_ANIO"] / row["EXISTENCIAS_CULIACAN"]) * row["RENTABILIDAD"],
        axis=1
    )

    df["Stock_Reabastecer"] = df["CANTIDAD_MES_ANTERIOR"] - \
        df["EXISTENCIAS_CULIACAN"]
    df["INDICE_PRIORIDAD_ACTUAL"] = df["Stock_Reabastecer"] * df["RENTABILIDAD"]

    # Determinar si el orden es ascendente o descendente
    ascending = sort_order != 'desc'

    # Mapeo de nombres de columnas en la tabla a nombres de columnas en el DataFrame
    column_mapping = {
        'Producto': 'DESCRI',
        'Existencia': 'EXISTENCIAS_CULIACAN',
        'Rentabilidad': 'RENTABILIDAD',
        'Prioridad_actual': 'INDICE_PRIORIDAD_ACTUAL',
        'Prioridad_anual': 'INDICE_PRIORIDAD_ANUAL',
        'Cantidad_ultimo_anio': 'CANTIDAD_ULTIMO_ANIO',
        'Cantidad_mes_anterior': 'CANTIDAD_MES_ANTERIOR'
    }

    # Convertir el nombre de la columna de la tabla al nombre de la columna en el DataFrame
    sort_column = column_mapping.get(sort_by, sort_by)

    # Ordenar el DataFrame
    df_sorted = df.sort_values(by=sort_column, ascending=ascending)

    # Obtener todas las líneas de producción únicas para el dropdown
    lineas_produccion = sorted(
        df_sorted["NOM_LINEA_PRODUCCION"].unique().tolist())

    # Filtrar el DataFrame si se ha seleccionado una línea de producción
    if linea_produccion_seleccionada:
        df_sorted = df_sorted[df_sorted["NOM_LINEA_PRODUCCION"]
                              == linea_produccion_seleccionada]

    # Obtener productos, índices de prioridad y existencias
    productos = df_sorted["DESCRI"].tolist()
    indice_prioridad_actual_list = df_sorted["INDICE_PRIORIDAD_ACTUAL"].tolist(
    )
    indice_prioridad_anual_list = df_sorted["INDICE_PRIORIDAD_ANUAL"].tolist()
    existencias = df_sorted["EXISTENCIAS_CULIACAN"].tolist()
    rentabilidad = df_sorted["RENTABILIDAD"].tolist()
    lineas_prod = df_sorted["NOM_LINEA_PRODUCCION"].tolist()
    cantidad_ultimo_anio = df_sorted["CANTIDAD_ULTIMO_ANIO"].tolist()
    cantidad_mes_anterior = df_sorted["CANTIDAD_MES_ANTERIOR"].tolist()

    # Fecha de inicio para el calendario de producción
    fecha_inicio = datetime.date.today()

    # Días de la semana
    dias_semana = ["Lunes", "Martes", "Miércoles",
                   "Jueves", "Viernes", "Sábado"]
    calendario_produccion = []

    # Asignar productos a cada día
    for i, (producto, indice_prioridad_actual, indice_prioridad_anual, existencia, rentabilidad, linea_prod, cantidad_ultimo_anio, cantidad_mes_anterior) in enumerate(
            zip(productos, indice_prioridad_actual_list, indice_prioridad_anual_list, existencias, rentabilidad, lineas_prod, cantidad_ultimo_anio, cantidad_mes_anterior)):
        dia_produccion = dias_semana[i % 6]  # Ciclo de lunes a sábado
        fecha_produccion = fecha_inicio + datetime.timedelta(
            days=i // 6 * 7 + i % 6
        )  # Sumar días para cada semana

        # Formatear el índice de prioridad con separador de miles y dos decimales
        indice_prioridad_actual_formateado = "{:,.2f}".format(
            float(indice_prioridad_actual))
        indice_prioridad_anual_formateado = "{:,.2f}".format(
            float(indice_prioridad_anual))

        existencia_formateada = "{:,.2f}".format(float(existencia))
        cantidad_ultimo_anio_formateada = "{:,.2f}".format(
            float(cantidad_ultimo_anio))
        cantidad_mes_anterior_formateada = "{:,.2f}".format(
            float(cantidad_mes_anterior))

        calendario_produccion.append(
            {
                "Fecha": fecha_produccion.strftime("%Y-%m-%d"),
                "Existencia": existencia_formateada,
                "Día": dia_produccion,
                "Producto": producto,
                "Indice_Prioridad_Actual": indice_prioridad_actual_formateado,
                "Indice_Prioridad_Anual": indice_prioridad_anual_formateado,
                "Rentabilidad": rentabilidad,
                "Cantidad_ultimo_anio": cantidad_ultimo_anio_formateada,
                "Cantidad_mes_anterior": cantidad_mes_anterior_formateada
            }
        )

    # Devolver un diccionario con todos los datos transformados
    return {
        'calendario_produccion': calendario_produccion,
        'lineas_produccion': lineas_produccion
    }


def transform_plan_produccion_por_articulo_data(data, sort_by='INDICE', sort_order='desc', linea_produccion_seleccionada=''):
    """
    Transforma los datos de producción aplicando cálculos y filtros

    Args:
        data: Datos obtenidos de la API
        sort_by: Columna por la que ordenar los datos
        sort_order: Orden de clasificación ('asc' o 'desc')
        linea_produccion_seleccionada: Línea de producción para filtrar

    Returns:
        Diccionario con los datos transformados y metadatos
    """
    # Convertir a DataFrame
    df = pd.DataFrame(data)

    # Obtener todas las líneas de producción únicas para el dropdown ANTES de filtrar
    lineas_produccion = sorted(
        df["NOM_LINEA_PRODUCCION"].unique().tolist())

    # Filtrar el DataFrame si se ha seleccionado una línea de producción
    if linea_produccion_seleccionada:
        df = df[df["NOM_LINEA_PRODUCCION"]
                == linea_produccion_seleccionada]

    # Constantes
    DIAS_PLANIFICACION = 14  # Dos semanas

    # Calcular métricas base
    df["Venta diaria promedio"] = df["CANTIDAD_ULTIMO_ANIO"] / 365
    df["Venta esperada periodo"] = (
        df["CANTIDAD_MES_ANTERIOR"] /
        30 * DIAS_PLANIFICACION
    )

    # Calcular coberturas de inventario
    df["Cobertura matriz"] = df["EXISTENCIAS_MATRIZ"] / \
        df["Venta diaria promedio"]
    df["Cobertura sucursales"] = df["EXISTENCIAS_SUCURSALES"] / \
        df["Venta diaria promedio"]
    df["Cobertura total"] = df["Cobertura matriz"] + df["Cobertura sucursales"]

    # Calcular déficit considerando existencias en sucursales
    df["Deficit inventario"] = df.apply(
        lambda row: (
            # Si no hay stock local pero hay en sucursales, déficit reducido
            max(0, DIAS_PLANIFICACION - row["Cobertura matriz"]) * 0.3
            if row["EXISTENCIAS_MATRIZ"] == 0
            and row["Cobertura sucursales"] > DIAS_PLANIFICACION
            # Si no hay stock local y poco en sucursales, déficit alto
            else (
                max(0, DIAS_PLANIFICACION - row["Cobertura matriz"])
                if row["Cobertura total"] < DIAS_PLANIFICACION
                # Si hay suficiente stock total, déficit bajo
                else max(0, (DIAS_PLANIFICACION - row["Cobertura matriz"]) * 0.5)
            )
        ),
        axis=1,
    )

    # Normalización de variables
    scaler = MinMaxScaler()
    df["Deficit normalizado"] = scaler.fit_transform(
        df[["Deficit inventario"]])
    df["Rentabilidad normalizada"] = scaler.fit_transform(
        df[["RENTABILIDAD_ULTIMO_ANIO"]])
    df["Venta esperada normalizada"] = scaler.fit_transform(
        df[["Venta esperada periodo"]])

    # Calcular índice de prioridad
    df["Índice de Prioridad Ajustado"] = (
        (df["Deficit normalizado"] * 0.5)  # 50% peso al déficit de inventario
        + (df["Rentabilidad normalizada"] * 0.3)  # 30% peso a la rentabilidad
        # 20% peso a la venta esperada
        + (df["Venta esperada normalizada"] * 0.2)
    )

    # Mapeo de nombres de columnas en la tabla a nombres de columnas en el DataFrame
    column_mapping = {
        'Artículo': 'DESCRI',
        'Producto': 'NOM_PRODUCTO',
        'Rentabilidad': 'RENTABILIDAD_ULTIMO_ANIO',
        'Cantidad Año': 'CANTIDAD_ULTIMO_ANIO',
        'Cantidad Mes': 'CANTIDAD_MES_ANTERIOR',
        'Stock matriz': 'EXISTENCIAS_MATRIZ',
        'Stock Suc': 'EXISTENCIAS_SUCURSALES',
        'Stock Obs': 'EXISTENCIAS_OBSERVACION',
        'Cob Local': 'Cobertura matriz',
        'Cob Suc': 'Cobertura sucursales',
        'Índice': 'Índice de Prioridad Ajustado',
        'Recomendación': 'Recomendación Ajustada',
        'COD_ART': 'COD_ART',
        'Fecha espera': 'FECHA_ESPERA'
    }

    # Agregar recomendación considerando stock en sucursales antes del ordenamiento
    df["Recomendación Ajustada"] = df.apply(
        lambda row: (
            "URGENTE - Sin stock"
            if row["EXISTENCIAS_MATRIZ"] == 0
            and row["Cobertura sucursales"] < DIAS_PLANIFICACION
            else (
                "MEDIA - Trasladar de sucursales"
                if row["EXISTENCIAS_MATRIZ"] == 0
                and row["Cobertura sucursales"] >= DIAS_PLANIFICACION
                else (
                    "ALTA - Producir"
                    if row["Cobertura matriz"] < 7
                    else (
                        "MEDIA - Monitorear"
                        if row["Cobertura matriz"] < 15
                        else "BAJA - Stock suficiente"
                    )
                )
            )
        ),
        axis=1,
    )

    # Convertir el nombre de la columna de la tabla al nombre de la columna en el DataFrame
    sort_column = column_mapping.get(sort_by, 'Índice de Prioridad Ajustado')

    # Determinar si el orden es ascendente o descendente
    ascending = sort_order != 'desc'

    # Ordenar el DataFrame según la columna seleccionada
    if sort_column in df.columns:
        df_sorted = df.sort_values(by=sort_column, ascending=ascending)
    else:
        # Si la columna no existe, ordenar por el índice de prioridad por defecto
        df_sorted = df.sort_values(
            "Índice de Prioridad Ajustado", ascending=False)

    data = []
    for index, row in df_sorted.iterrows():
        # Formatear la fecha FECHA_ESPERA al formato dd-mmm-yy
        fecha_espera_formateada = ""
        if pd.notna(row["FECHA_ESPERA"]):
            try:
                # Convertir a datetime si es string
                if isinstance(row["FECHA_ESPERA"], str):
                    fecha_espera = pd.to_datetime(row["FECHA_ESPERA"])
                else:
                    fecha_espera = row["FECHA_ESPERA"]

                # Formatear la fecha
                dia = fecha_espera.day
                # Lista de nombres de meses abreviados en español
                meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                         'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
                mes = meses[fecha_espera.month - 1]
                # Obtener los últimos dos dígitos del año
                anio = str(fecha_espera.year)[-2:]

                fecha_espera_formateada = f"{dia:02d}-{mes}-{anio}"
            except:
                fecha_espera_formateada = str(row["FECHA_ESPERA"])

        data.append({
            "COD_ART": row["COD_ART"],
            "ARTICULO": row["DESCRI"],
            "NOM_PRODUCTO": row["NOM_PRODUCTO"],
            "FECHA_ESPERA": fecha_espera_formateada,
            "CANTIDAD_ULTIMO_ANIO": "{:,.2f}".format(row["CANTIDAD_ULTIMO_ANIO"]),
            "VENTA_ULTIMO_ANIO": "{:,.2f}".format(row["VENTA_ULTIMO_ANIO"]),
            "COSTO_ULTIMO_ANIO": "{:,.2f}".format(row["COSTO_ULTIMO_ANIO"]),
            "UTILIDAD_ULTIMO_ANIO": "{:,.2f}".format(row["UTILIDAD_ULTIMO_ANIO"]),
            "RENTABILIDAD_ULTIMO_ANIO": "{:,.2f}".format(row["RENTABILIDAD_ULTIMO_ANIO"]),
            "CANTIDAD_MES_ANTERIOR": "{:,.2f}".format(row["CANTIDAD_MES_ANTERIOR"]),
            "VENTA_MES_ANTERIOR": "{:,.2f}".format(row["VENTA_MES_ANTERIOR"]),
            "COSTO_MES_ANTERIOR": "{:,.2f}".format(row["COSTO_MES_ANTERIOR"]),
            "UTILIDAD_MES_ANTERIOR": "{:,.2f}".format(row["UTILIDAD_MES_ANTERIOR"]),
            "RENTABILIDAD_MES_ANTERIOR": "{:,.2f}".format(row["RENTABILIDAD_MES_ANTERIOR"]),
            "EXISTENCIAS_MATRIZ": "{:,.2f}".format(row["EXISTENCIAS_MATRIZ"]),
            "EXISTENCIAS_SUCURSALES": "{:,.2f}".format(row["EXISTENCIAS_SUCURSALES"]),
            "EXISTENCIAS_OBSERVACION": "{:,.2f}".format(row["EXISTENCIAS_OBSERVACION"]),
            "NOM_LINEA_PRODUCCION": row["NOM_LINEA_PRODUCCION"],
            "VENTA_DIARIA_PROMEDIO": "{:,.2f}".format(row["Venta diaria promedio"]),
            "VENTA_ESPERADA_PERIODO": "{:,.2f}".format(row["Venta esperada periodo"]),
            "COBERTURA_MATRIZ": "{:,.2f}".format(row["Cobertura matriz"]),
            "COBERTURA_SUCURSALES": "{:,.2f}".format(row["Cobertura sucursales"]),
            "COBERTURA_TOTAL": "{:,.2f}".format(row["Cobertura total"]),
            "DEFICIT_INVENTARIO": "{:,.2f}".format(row["Deficit inventario"]),
            "DEFICIT_NORMALIZADO": "{:,.2f}".format(row["Deficit normalizado"]),
            "RENTABILIDAD_NORMALIZADA": "{:,.2f}".format(row["Rentabilidad normalizada"]),
            "VENTA_ESPERADA_NORMALIZADA": "{:,.2f}".format(row["Venta esperada normalizada"]),
            "ÍNDICE_DE_PRIORIDAD_AJUSTADO": "{:,.2f}".format(row["Índice de Prioridad Ajustado"]),
            "RECOMENDACIÓN_AJUSTADA": row["Recomendación Ajustada"]
        })

    return {
        'data': data,
        'lineas_produccion': lineas_produccion
    }
