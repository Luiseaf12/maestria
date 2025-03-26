from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
# Generar datos simulados para clasificación
np.random.seed(42)
X = np.random.rand(200, 3)  # 200 instancias, 3 atributos
y = np.random.randint(0, 2, 200)  # Clases binarias (0 o 1)

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Crear y entrenar un modelo de clasificación (Random Forest)
modelo = RandomForestClassifier(n_estimators=10, random_state=42)
modelo.fit(X_train, y_train)

# Hacer predicciones y evaluar el modelo
y_pred = modelo.predict(X_test)
precision = accuracy_score(y_test, y_pred)

# Mostrar resultados del modelo
resultado = {"Precisión del Modelo (%)": precision * 100}
df_resultado = pd.DataFrame([resultado])

print("\nResultados de la Evaluación del Modelo:")
print("-" * 50)
print(df_resultado.to_string(index=False))
