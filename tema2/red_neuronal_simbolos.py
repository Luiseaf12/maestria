import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# Entrada: bitmaps de 3x3 (convertidos a vectores de 9)
X = np.array(
    [
        [0, 1, 0, 1, 1, 1, 0, 1, 0],  # "+"
        [0, 0, 0, 1, 1, 1, 0, 0, 0],  # "-"
        [1, 1, 1, 0, 0, 0, 1, 1, 1],  # "="
    ]
)

# Salida: clase codificada como one-hot
# "+" = 0, "-" = 1, "=" = 2
y = to_categorical([0, 1, 2], num_classes=3)

# Construcción del modelo
model = Sequential()
model.add(Dense(2, input_dim=9, activation="relu"))  # Capa oculta de 2 neuronas
model.add(
    Dense(3, activation="softmax")
)  # Capa de salida con 3 neuronas (una por clase)

# Compilación
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Entrenamiento
model.fit(X, y, epochs=200, verbose=0)

# Evaluación
loss, accuracy = model.evaluate(X, y, verbose=0)
print(f"Precisión del modelo: {accuracy * 100:.2f}%")

# Prueba
predicciones = model.predict(X)
for i, pred in enumerate(predicciones):
    clase = np.argmax(pred)
    simbolo = ["+", "-", "="][clase]
    print(f"Entrada {i+1}: Predicción → {simbolo} (Probabilidades: {pred})")
