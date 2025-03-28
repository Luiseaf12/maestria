import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

# Crear el DataFrame a partir de los datos de la imagen
data = {
    "Ambiente": [
        "Soleado",
        "Soleado",
        "Nublado",
        "Lluvioso",
        "Lluvioso",
        "Lluvioso",
        "Nublado",
        "Soleado",
        "Soleado",
        "Lluvioso",
        "Soleado",
        "Nublado",
        "Nublado",
        "Lluvioso",
    ],
    "Temperatura": [
        "Alta",
        "Alta",
        "Alta",
        "Media",
        "Baja",
        "Baja",
        "Baja",
        "Media",
        "Baja",
        "Media",
        "Media",
        "Media",
        "Alta",
        "Media",
    ],
    "Humedad": [
        "Alta",
        "Alta",
        "Alta",
        "Alta",
        "Normal",
        "Normal",
        "Normal",
        "Alta",
        "Normal",
        "Normal",
        "Normal",
        "Alta",
        "Normal",
        "Alta",
    ],
    "Viento": [
        "Falso",
        "Verdadero",
        "Falso",
        "Falso",
        "Falso",
        "Verdadero",
        "Verdadero",
        "Falso",
        "Falso",
        "Falso",
        "Verdadero",
        "Verdadero",
        "Falso",
        "Verdadero",
    ],
    "Clase": [
        "No",
        "No",
        "Sí",
        "Sí",
        "Sí",
        "No",
        "Sí",
        "No",
        "Sí",
        "Sí",
        "Sí",
        "Sí",
        "Sí",
        "No",
    ],
}

df = pd.DataFrame(data)

# Codificar las variables categóricas
df_encoded = pd.get_dummies(df.drop("Clase", axis=1))
y = df["Clase"].map({"No": 0, "Sí": 1})

# Crear el clasificador y entrenarlo
clf = DecisionTreeClassifier(criterion="entropy", random_state=0)
clf.fit(df_encoded, y)

# Exportar el árbol como texto
tree_rules = export_text(clf, feature_names=list(df_encoded.columns))
tree_rules
print(tree_rules)
