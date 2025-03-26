from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np

# Crear dataset simulado para reposición de stock
data = {
    "Stock_Actual": [5, 20, 3, 50, 10, 2, 40, 1, 8, 15],
    "Frecuencia_Ventas": [15, 5, 20, 3, 12, 25, 2, 30, 18, 7],
    "Días_Promedio_Venta": [2, 10, 1, 15, 3, 1, 20, 0.5, 2, 7],
    "Temporada": [1, 0, 1, 0, 1, 1, 0, 1, 1, 0],  # 1=Alta demanda, 0=Baja demanda
    "Relacionado_Con_Otro": [1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
    "Reponer": [1, 0, 1, 0, 1, 1, 0, 1, 1, 0]  # 1=Reponer, 0=No reponer
}

# Convertir a DataFrame
df = pd.DataFrame(data)

# Separar variables independientes y dependientes
X = df.drop(columns=["Reponer"])
y = df["Reponer"]

# Crear y entrenar el Árbol de Decisión
modelo = DecisionTreeClassifier(criterion="entropy", random_state=42)
modelo.fit(X, y)

# Simular una nueva predicción de stock
nueva_data = pd.DataFrame({
    "Stock_Actual": [4],  # Quedan 4 unidades
    "Frecuencia_Ventas": [18],  # Se venden rápido
    "Días_Promedio_Venta": [2],  # En 2 días se agotará
    "Temporada": [1],  # Alta demanda
    "Relacionado_Con_Otro": [1]  # Se vende con otro producto
})

# Hacer la predicción
prediccion = modelo.predict(nueva_data)
resultado = "Sí, reponer stock" if prediccion[0] == 1 else "No es necesario reponer aún"
print(resultado)
