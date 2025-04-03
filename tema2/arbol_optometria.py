from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Paso 1: Crear el conjunto de datos
data = [
    ["Joven", "Miopía", "Sí", "Reducido", "Duras"],
    ["Joven", "Miopía", "Sí", "Normal", "Duras"],
    ["Joven", "Hipermetropía", "No", "Reducido", "Duras"],
    ["Joven", "Hipermetropía", "No", "Normal", "Blandas"],
    ["Pre-presbicia", "Miopía", "Sí", "Reducido", "Blandas"],
    ["Pre-presbicia", "Miopía", "Sí", "Normal", "Duras"],
    ["Pre-presbicia", "Hipermetropía", "No", "Reducido", "Duras"],
    ["Pre-presbicia", "Hipermetropía", "No", "Normal", "Blandas"],
    ["Presbicia", "Miopía", "Sí", "Reducido", "Blandas"],
    ["Presbicia", "Miopía", "Sí", "Normal", "Duras"],
    ["Presbicia", "Hipermetropía", "No", "Reducido", "Duras"],
    ["Presbicia", "Hipermetropía", "No", "Normal", "Blandas"],
]

columns = ["Edad", "Prescripción", "Astigmatismo", "Lágrima", "Clase"]
df = pd.DataFrame(data, columns=columns)

# Paso 2: Codificar los datos categóricos
label_encoders = {}
df_encoded = df.copy()

for column in df_encoded.columns:
    le = LabelEncoder()
    df_encoded[column] = le.fit_transform(df_encoded[column])
    label_encoders[column] = le

# Paso 3: Separar características y etiqueta
X = df_encoded.drop("Clase", axis=1)
y = df_encoded["Clase"]


# Paso 4: Entrenar el árbol de decisión (ID3 con entropía)
clf = DecisionTreeClassifier(criterion="entropy", random_state=0)
clf.fit(X, y)

# Paso 5: Mostrar el árbol como texto
tree_rules = export_text(clf, feature_names=X.columns.tolist())
print("Árbol de decisión:\n")
print(tree_rules)
# print(label_encoders["Edad"].classes_)
