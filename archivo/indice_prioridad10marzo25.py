# Crear el DataFrame con los datos proporcionados
import pandas as pd

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
        "Producto": "Cyromax ",
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
        "Existencia local": 0,
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

# Crear el DataFrame
df = pd.DataFrame(data)

# Calcular utilidad total
df["Utilidad Total"] = df["ventas en cantidad del ultimo año"] * df["Rentabilidad"]

# Calcular el índice de prioridad
df["Índice de Prioridad"] = df.apply(
    lambda row: (
        row["Utilidad Total"]
        if row["Existencia local"] == 0
        else (row["ventas en cantidad del ultimo año"] / row["Existencia local"])
        * row["Rentabilidad"]
    ),
    axis=1,
)

# Ordenar por el índice de prioridad de mayor a menor
df_sorted = df.sort_values(by="Índice de Prioridad", ascending=False)

# Mostrar los resultados
print("\nProductos ordenados por índice de prioridad:")
print(
    df_sorted[["Producto", "Existencia local", "Utilidad Total", "Índice de Prioridad"]]
)
