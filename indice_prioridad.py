import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Datos
data = [
    {
        "Producto": "Vibe ph",
        "Existencia local": 3000,
        "Existencia sucursales": 1000,
        "ventas en cantidad del ultimo año": 89388,
        "ventas en cantidad de este mes en el año pasado": 888,
        "Rentabilidad": 0.5,
    },
    {
        "Producto": "Cyromax",
        "Existencia local": 97,
        "Existencia sucursales": 103,
        "ventas en cantidad del ultimo año": 3114,
        "ventas en cantidad de este mes en el año pasado": 311,
        "Rentabilidad": 0.4,
    },
    {
        "Producto": "Cym m8",
        "Existencia local": 1016,
        "Existencia sucursales": 106,
        "ventas en cantidad del ultimo año": 12301,
        "ventas en cantidad de este mes en el año pasado": 1231,
        "Rentabilidad": 0.3,
    },
    {
        "Producto": "Benolate",
        "Existencia local": 200,
        "Existencia sucursales": 100,
        "ventas en cantidad del ultimo año": 4996,
        "ventas en cantidad de este mes en el año pasado": 499,
        "Rentabilidad": 0.2,
    },
    {
        "Producto": "Strepto 51",
        "Existencia local": 712,
        "Existencia sucursales": 1000,
        "ventas en cantidad del ultimo año": 7040,
        "ventas en cantidad de este mes en el año pasado": 704,
        "Rentabilidad": 0.4,
    },
    {
        "Producto": "Killher",
        "Existencia local": 0,
        "Existencia sucursales": 100,
        "ventas en cantidad del ultimo año": 100,
        "ventas en cantidad de este mes en el año pasado": 10,
        "Rentabilidad": 0.10,
    },
]

# Constantes
DIAS_TRASLADO = 5
COSTO_TRASLADO_PORCENTAJE = 0.01  # 1% del valor del producto
DIAS_PLANIFICACION = 14  # Dos semanas

# Crear el DataFrame
df = pd.DataFrame(data)

# Calcular métricas base
df["Venta diaria promedio"] = df["ventas en cantidad del ultimo año"] / 365
df["Venta esperada periodo"] = (
    df["ventas en cantidad de este mes en el año pasado"] / 30 * DIAS_PLANIFICACION
)

# Calcular coberturas de inventario
df["Cobertura actual"] = df["Existencia local"] / df["Venta diaria promedio"]
df["Cobertura sucursales"] = df["Existencia sucursales"] / \
    df["Venta diaria promedio"]
df["Cobertura total"] = df["Cobertura actual"] + df["Cobertura sucursales"]

# Calcular déficit considerando existencias en sucursales
df["Deficit inventario"] = df.apply(
    lambda row: (
        # Si no hay stock local pero hay en sucursales, déficit reducido
        max(0, DIAS_PLANIFICACION - row["Cobertura actual"]) * 0.3
        if row["Existencia local"] == 0
        and row["Cobertura sucursales"] > DIAS_PLANIFICACION
        # Si no hay stock local y poco en sucursales, déficit alto
        else (
            max(0, DIAS_PLANIFICACION - row["Cobertura actual"])
            if row["Cobertura total"] < DIAS_PLANIFICACION
            # Si hay suficiente stock total, déficit bajo
            else max(0, (DIAS_PLANIFICACION - row["Cobertura actual"]) * 0.5)
        )
    ),
    axis=1,
)

# Normalización de variables
scaler = MinMaxScaler()
df["Deficit normalizado"] = scaler.fit_transform(df[["Deficit inventario"]])
df["Rentabilidad normalizada"] = scaler.fit_transform(df[["Rentabilidad"]])
df["Venta esperada normalizada"] = scaler.fit_transform(
    df[["Venta esperada periodo"]])

# Calcular índice de prioridad
df["Índice de Prioridad Ajustado"] = (
    (df["Deficit normalizado"] * 0.5)  # 50% peso al déficit de inventario
    + (df["Rentabilidad normalizada"] * 0.3)  # 30% peso a la rentabilidad
    + (df["Venta esperada normalizada"] * 0.2)  # 20% peso a la venta esperada
)

# Ordenar por prioridad
df_sorted = df.sort_values("Índice de Prioridad Ajustado", ascending=False)

# Agregar recomendación considerando stock en sucursales
df_sorted["Recomendación Ajustada"] = df_sorted.apply(
    lambda row: (
        "URGENTE - Sin stock"
        if row["Existencia local"] == 0
        and row["Cobertura sucursales"] < DIAS_PLANIFICACION
        else (
            "MEDIA - Trasladar de sucursales"
            if row["Existencia local"] == 0
            and row["Cobertura sucursales"] >= DIAS_PLANIFICACION
            else (
                "ALTA - Stock bajo"
                if row["Cobertura actual"] < 7
                else (
                    "MEDIA - Monitorear"
                    if row["Cobertura actual"] < 15
                    else "BAJA - Stock suficiente"
                )
            )
        )
    ),
    axis=1,
)

# Renombrar columnas para mejor visualización
columnas_mostrar = {
    "Producto": "Producto",
    "Rentabilidad": "Ut%",
    "ventas en cantidad del ultimo año": "Ventas Año",
    "ventas en cantidad de este mes en el año pasado": "Ventas Mes",
    "Existencia local": "Stock matriz",
    "Existencia sucursales": "Stock Suc",
    "Cobertura actual": "Cob Local",
    "Cobertura sucursales": "Cob Suc",
    "Índice de Prioridad Ajustado": "Índice",
    "Recomendación Ajustada": "Recomendación",
}

# Mostrar resultados
print("\nPrioridad de producción:")
df_mostrar = df_sorted[columnas_mostrar.keys()].copy()
df_mostrar.rename(columns=columnas_mostrar, inplace=True)

# Configurar formato de decimales
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.float_format", lambda x: "%.2f" % x)

print(df_mostrar.to_string(index=False))
