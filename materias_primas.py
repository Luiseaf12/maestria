import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def calcular_viabilidad_demanda(
    demanda_anual: float,
    demanda_semestre: float,
    pedidos_confirmados: float = None,
    meses_datos: int = 12,
) -> float:
    """
    Calcula la viabilidad de la demanda basada en:
    1. Consistencia entre demanda anual y semestral
    2. Existencia de pedidos confirmados
    3. Cantidad de meses con datos históricos

    Args:
        demanda_anual: Demanda total anual
        demanda_semestre: Demanda del último semestre
        pedidos_confirmados: Cantidad de pedidos ya confirmados (opcional)
        meses_datos: Cantidad de meses con datos históricos (default 12)

    Returns:
        float: Índice de viabilidad entre 0 y 1
    """
    # 1. Consistencia entre demanda anual y semestral (40% del peso)
    demanda_semestre_esperada = demanda_anual / 2
    ratio_consistencia = (
        min(demanda_semestre / demanda_semestre_esperada, 1)
        if demanda_semestre_esperada > 0
        else 0
    )
    peso_consistencia = 0.4

    # 2. Pedidos confirmados (35% del peso)
    peso_pedidos = 0.35
    if pedidos_confirmados is None:
        ratio_pedidos = 0.5  # Valor neutral si no hay datos
    else:
        ratio_pedidos = min(pedidos_confirmados / (demanda_anual / 12), 1)

    # 3. Histórico de datos (25% del peso)
    peso_historico = 0.25
    ratio_historico = min(meses_datos / 12, 1)

    # Cálculo final ponderado
    viabilidad = (
        ratio_consistencia * peso_consistencia
        + ratio_pedidos * peso_pedidos
        + ratio_historico * peso_historico
    )

    return round(viabilidad, 2)


# Datos de productos con existencias y demanda
productos = [
    {
        "Producto": "Aromina",
        "Stock actual": 11000,
        "Stock máximo": 30000,
        "Compra mínima": 20000,
        "Tiempo reabastecimiento": 14,
        "Demanda anual": 67720,
        "Demanda semestre pasado": 42000,
        "compra por stock": "si",
    },
    {
        "Producto": "map 015",
        "Stock actual": 3679,
        "Stock máximo": 5000,
        "Compra mínima": 500,
        "Tiempo reabastecimiento": 180,
        "Demanda anual": 2467,
        "Demanda semestre pasado": 1500,
        "compra por stock": "no",
    },
    {
        "Producto": "Cymoxanil",
        "Stock actual": 1016,
        "Stock máximo": 2000,
        "Compra mínima": 300,
        "Tiempo reabastecimiento": 180,
        "Demanda anual": 12301,
        "Demanda semestre pasado": 7386,
        "compra por stock": "no",
    },
    {
        "Producto": "Benomilo",
        "Stock actual": 200,
        "Stock máximo": 1000,
        "Compra mínima": 200,
        "Tiempo reabastecimiento": 60,
        "Demanda anual": 4996,
        "Demanda semestre pasado": 2998,
        "compra por stock": "no",
    },
    {
        "Producto": "Streptomicina",
        "Stock actual": 712,
        "Stock máximo": 1500,
        "Compra mínima": 250,
        "Tiempo reabastecimiento": 25,
        "Demanda anual": 7040,
        "Demanda semestre pasado": 4224,
        "compra por stock": "no",
    },
    {
        "Producto": "dimetomorf",
        "Stock actual": 0,
        "Stock máximo": 300,
        "Compra mínima": 100,
        "Tiempo reabastecimiento": 90,
        "Demanda anual": 100,
        "Demanda semestre pasado": 60,
        "compra por stock": "no",
    },
]

# Constantes
DIAS_PLANIFICACION = 180  # Días de planificación de compra

# Crear DataFrame
df = pd.DataFrame(productos)

# Calcular viabilidad de demanda
df["Viabilidad demanda"] = df.apply(
    lambda row: calcular_viabilidad_demanda(
        demanda_anual=row["Demanda anual"],
        demanda_semestre=row["Demanda semestre pasado"],
    ),
    axis=1,
)

# Cálculo de demanda diaria y demanda esperada
df["Demanda diaria promedio"] = df["Demanda anual"] / 365
df["Demanda esperada"] = df["Demanda semestre pasado"]

# Cálculo de cobertura de inventario
df["Cobertura actual"] = df["Stock actual"] / df["Demanda diaria promedio"]

# Verificar si la compra mínima es viable
df["Compra viable"] = df.apply(
    lambda row: (
        "SI"
        if (row["Stock actual"] + row["Compra mínima"]) <= row["Stock máximo"]
        else "NO"
    ),
    axis=1,
)

# Cálculo del déficit de inventario
df["Déficit de compra"] = df.apply(
    lambda row: max(0, DIAS_PLANIFICACION - row["Cobertura actual"]), axis=1
)

# Calcular cantidad sugerida de compra
df["Cantidad sugerida"] = df.apply(
    lambda row: (
        # Si es compra por stock y es viable, sugerir compra mínima
        row["Compra mínima"]
        if row["compra por stock"].lower() == "si"
        and (row["Stock actual"] + row["Compra mínima"]) <= row["Stock máximo"]
        else (
            # Si no es compra por stock, calcular óptimo para 6 meses
            min(
                max(
                    0,
                    round(
                        (
                            row["Demanda diaria promedio"] * DIAS_PLANIFICACION
                        )  # Demanda esperada 6 meses
                        - row["Stock actual"]  # Restar stock actual
                    ),
                ),
                row["Stock máximo"] - row["Stock actual"],  # No exceder stock máximo
            )
        )
    ),
    axis=1,
)

# Normalización de variables para la prioridad
scaler = MinMaxScaler()
df["Déficit normalizado"] = scaler.fit_transform(df[["Déficit de compra"]])
df["Demanda normalizada"] = scaler.fit_transform(df[["Demanda esperada"]])
df["Viabilidad normalizada"] = scaler.fit_transform(df[["Viabilidad demanda"]])

# Cálculo del índice de prioridad de compra
df["Índice de Compra"] = (
    df["Déficit normalizado"] * 0.5  # 50% peso al déficit
    + df["Demanda normalizada"] * 0.2  # 20% peso a la demanda esperada
    + df["Viabilidad normalizada"] * 0.2  # 20% peso a la viabilidad de la demanda
    + (1 - df["Viabilidad normalizada"])
    * 0.1  # 10% peso a la obsolescencia (productos menos obsoletos tienen más prioridad)
)

# Ordenar por prioridad de compra
df_sorted = df.sort_values("Índice de Compra", ascending=False)

# Generar recomendaciones
df_sorted["Recomendación"] = df_sorted.apply(
    lambda row: (
        "COMPRAR LOTE MÍNIMO"
        if row["compra por stock"].lower() == "si"
        and (row["Stock actual"] + row["Compra mínima"]) <= row["Stock máximo"]
        else (
            "COMPRA URGENTE"
            if row["Cobertura actual"] < 7
            else (
                "COMPRA ALTA"
                if row["Cobertura actual"] < 15
                else (
                    "COMPRA MEDIA"
                    if row["Cobertura actual"] < 30
                    else "SIN COMPRA - Stock suficiente"
                )
            )
        )
    ),
    axis=1,
)

# Renombrar columnas para mejor visualización
columnas_mostrar = {
    "Producto": "Producto",
    "Stock actual": "Stock Local",
    "Stock máximo": "Stock Máximo",
    "Compra mínima": "Mínimo",
    "Compra viable": "Viable",
    "Cobertura actual": "Cob Local",
    "Cantidad sugerida": "Comprar",
    "Índice de Compra": "Índice",
    "Recomendación": "Recomendación",
}

df_mostrar = df_sorted[columnas_mostrar.keys()].copy()
df_mostrar.rename(columns=columnas_mostrar, inplace=True)

# Mostrar resultados
print("\nSistema de Priorización de Compras")
print("=" * 100)
print("Fecha de análisis:", pd.Timestamp.now().strftime("%Y-%m-%d"))
print("Días de planificación:", DIAS_PLANIFICACION)
print("=" * 100)
print("\nResultados ordenados por índice de prioridad:")
print("-" * 100)
print(df_mostrar.to_string(index=False, float_format=lambda x: "{:.0f}".format(x)))
print("-" * 100)
print("\nNotas:")
print("- Cob Local: Días de cobertura con stock actual")
print("- Mínimo: Cantidad mínima de compra permitida")
print("- Viable: Indica si la compra mínima es posible sin exceder stock máximo")
print("- Comprar: Cantidad sugerida para cubrir los próximos 6 meses")
print("- Índice: Prioridad de compra (mayor valor = más prioritario)")
print("=" * 100)
