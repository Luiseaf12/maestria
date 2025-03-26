# Crear el DataFrame con los datos proporcionados
import pandas as pd

data = [
    {
        "Producto": "Vibe ph",
        "Existencia Actual": 4000,
        "Ventas Último Año": 89388,
        "Rentabilidad": 0.5,
        "Ventas último mes": 10000,
    },
    {
        "Producto": "Cyromax ",
        "Existencia Actual": 97,
        "Ventas Último Año": 3114,
        "Rentabilidad": 0.4,
        "Ventas último mes": 500,
    },
    {
        "Producto": "Cym m8",
        "Existencia Actual": 1016,
        "Ventas Último Año": 12301,
        "Rentabilidad": 0.3,
        "Ventas último mes": 1000,
    },
    {
        "Producto": "Benolate",
        "Existencia Actual": 0,
        "Ventas Último Año": 4996,
        "Rentabilidad": 0.2,
        "Ventas último mes": 1000
    },
    {
        "Producto": "Strepto 51",
        "Existencia Actual": 1712,
        "Ventas Último Año": 7040,
        "Rentabilidad": 0.4,
        "Ventas último mes": 2000,
    },
    {
        "Producto": "Killher",
        "Existencia Actual": 0,
        "Ventas Último Año": 100,
        "Rentabilidad": 0.10,
        "Ventas último mes": 20,
    },
]

# Crear el DataFrame
df = pd.DataFrame(data)

# print(df.info())  # Muestra información sobre tipos de datos y valores no nulos

# Calcular utilidad total
df["Utilidad Total"] = df["Ventas Último Año"] * df["Rentabilidad"]

df["Stock_Reabastecer"] = df["Ventas último mes"] - df["Existencia Actual"]

df["Índice de Prioridad"] = df["Stock_Reabastecer"] * df["Rentabilidad"]

# Ordenar por el índice de prioridad de mayor a menor
df_sorted = df.sort_values(by="Índice de Prioridad", ascending=False)

# Mostrar los resultados
print("\nProductos ordenados por índice de prioridad:")
print(df_sorted[["Producto", "Existencia Actual", "Ventas último mes", "Stock_Reabastecer",
      "Utilidad Total", "Índice de Prioridad"]])
