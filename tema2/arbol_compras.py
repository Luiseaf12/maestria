# caso  2 : Reglas de asociacion
# Si el usuario compra cipermetrina y  acidificante entonces recomendar foliar.
# Si el usuario compra azoxistrobin y metalaxil entonces recomendar foliar.
# Si el usuario compra acidificante y  azoxistrobin entonces recomendar antiespumante.

# Reejecutar el código después del reinicio del estado

from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import matplotlib.pyplot as plt
import pandas as pd

# Crear un conjunto de datos basado en las reglas de asociación
data = {
    "cipermetrina": [1, 0, 1, 0, 1, 0],
    "acidificante": [1, 0, 0, 0, 0, 1],
    "azoxistrobin": [0, 1, 0, 1, 1, 0],
    "metalaxil": [0, 1, 0, 1, 0, 1],
    "Recomendación": ["foliar", "foliar", "antiespumante", "foliar", "antiespumante", "foliar"]
}

# Convertir a DataFrame
df = pd.DataFrame(data)

# Codificar la variable objetivo a valores numéricos
target_mapping = {"foliar": 0, "antiespumante": 1}
df["Recomendación"] = df["Recomendación"].map(target_mapping)

# Dividir en variables de entrada y salida
X = df.drop(columns=["Recomendación"])
y = df["Recomendación"]

# Crear y entrenar el modelo de Árbol de Decisión
modelo = DecisionTreeClassifier(criterion="entropy", random_state=42)
modelo.fit(X, y)

# Visualizar el Árbol de Decisión
plt.figure(figsize=(10, 6))
tree.plot_tree(modelo, feature_names=X.columns, class_names=["foliar", "antiespumante"], filled=True)
plt.title("Árbol de Decisión para Reglas de Asociación")
plt.show()
