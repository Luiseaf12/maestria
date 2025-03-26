import pandas as pd
import numpy as np

data = [
    {"descripcion": "10-34-00", "pedida": 18070.00, "vendida": 16624.40, "formulada": 15720.90, "existencia": 5000.00},
    {"descripcion": "ABAMECTINA TECNICA 95%", "pedida": 743.97, "vendida": 684.45, "formulada": 647.25, "existencia": 200.50},
    {"descripcion": "ACEITE DE NEEM", "pedida": 0.00, "vendida": 0.00, "formulada": 0.00, "existencia": 0.00},
    {"descripcion": "ACIDO ACETICO GLACIAL 99.9%", "pedida": 2464.00, "vendida": 2266.88, "formulada": 2143.68, "existencia": 850.30},
    {"descripcion": "ACIDO ACETIL SALICILICO", "pedida": 90.00, "vendida": 82.80, "formulada": 78.30, "existencia": 25.00},
    {"descripcion": "ACIDO BORICO", "pedida": 2778.30, "vendida": 2556.53, "formulada": 2417.64, "existencia": 750.20},
    {"descripcion": "ACIDO CITRICO", "pedida": 1831.00, "vendida": 1776.52, "formulada": 1679.97, "existencia": 450.80},
    {"descripcion": "ACIDO DODECILBENCEN SULFONICO", "pedida": 3080.00, "vendida": 2833.62, "formulada": 2679.60, "existencia": 920.40},
    {"descripcion": "ACIDO FOSFORICO 54%", "pedida": 0.00, "vendida": 0.00, "formulada": 0.00, "existencia": 0.00},
    {"descripcion": "ACIDO FOSFORICO AL 52%", "pedida": 2200.00, "vendida": 2040.00, "formulada": 1914.00, "existencia": 580.50},
    {"descripcion": "ACIDO FOSFORICO ALIMENTICIO 80%", "pedida": 9856.00, "vendida": 9067.52, "formulada": 8574.72, "existencia": 2500.00},
    {"descripcion": "ACIDO GIBERELICO TEC. 90%", "pedida": 0.00, "vendida": 0.00, "formulada": 0.00, "existencia": 0.00},
    {"descripcion": "ACIDO INDOL BUTIRICO 97%", "pedida": 73.60, "vendida": 67.71, "formulada": 64.03, "existencia": 20.50},
    {"descripcion": "ACIDO NAFTALEN ACETICO 100%", "pedida": 90.07, "vendida": 82.86, "formulada": 78.75, "existencia": 25.80},
    {"descripcion": "ACIDO OXALICO", "pedida": 0.00, "vendida": 0.00, "formulada": 0.00, "existencia": 0.00},
    {"descripcion": "ACIDO SULFURICO 38%", "pedida": 14.68, "vendida": 13.51, "formulada": 12.77, "existencia": 5.20},
    {"descripcion": "ACIDOS FULVICOS LIQUIDO 750 GRSLT", "pedida": 5813.00, "vendida": 5347.96, "formulada": 5057.31, "existencia": 1500.00},
    {"descripcion": "ACIPLUS", "pedida": 500.00, "vendida": 460.00, "formulada": 435.00, "existencia": 150.30}
]

# Crear DataFrame
df = pd.DataFrame(data)

periodo = 30 
# Aplicar los criterios de cálculo
df["uso_promedio_diario"] = df["vendida"] / periodo  # Aproximando mes a 30 días
df["stock_seguridad"] = 1.96 * (df["vendida"] / periodo) * (7 ** 0.5)  # Nivel de servicio 95%, tiempo entrega 7 días
df["punto_reorden"] = (df["uso_promedio_diario"] * 7) + df["stock_seguridad"]
df["dias_inventario"] = df.apply(lambda row: row["existencia"] / row["uso_promedio_diario"] if row["uso_promedio_diario"] > 0 else 0, axis=1)
df["cantidad_a_comprar"] = df.apply(lambda row: max(row["punto_reorden"] - row["existencia"], 0), axis=1)

# Determinar prioridad y recomendación
def obtener_prioridad(row):
    if row["uso_promedio_diario"] == 0:
        return "Sin Movimiento"
    elif row["existencia"] <= row["stock_seguridad"]:
        return "URGENTE"
    elif row["existencia"] <= row["punto_reorden"]:
        return "ALTA"
    elif row["dias_inventario"] <= 30:
        return "MEDIA"
    else:
        return "BAJA"

df["prioridad"] = df.apply(obtener_prioridad, axis=1)

# Configurar formato de decimales
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.float_format", lambda x: "%.2f" % x)

# Renombrar columnas para mejor visualización
columnas_mostrar = {
    "descripcion": "Material",
    "existencia": "Existencia",
    "uso_promedio_diario": "Uso Diario",
    "dias_inventario": "Días Inv",
    "punto_reorden": "Punto Reorden",
    "cantidad_a_comprar": "Cant. Comprar",
    "prioridad": "Prioridad"
}

# Mostrar resultados
df_mostrar = df[columnas_mostrar.keys()].copy()
df_mostrar.rename(columns=columnas_mostrar, inplace=True)
df_mostrar = df_mostrar.sort_values(by=["Prioridad", "Cant. Comprar"], ascending=[True, False])
print("\nAnálisis de Materia Prima:")
print(df_mostrar.to_string(index=False))