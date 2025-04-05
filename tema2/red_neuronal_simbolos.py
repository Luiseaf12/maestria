import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, BatchNormalization
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
model.add(Dense(16, input_dim=9, activation="relu"))  # Primera capa oculta con 16 neuronas
model.add(BatchNormalization())
model.add(Dense(8, activation="relu"))  # Segunda capa oculta con 8 neuronas
model.add(BatchNormalization())
model.add(Dense(3, activation="softmax"))  # Capa de salida

# Compilación
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Entrenamiento con más épocas
model.fit(X, y, epochs=500, batch_size=1, verbose=0)

# Evaluación
loss, accuracy = model.evaluate(X, y, verbose=0)
print(f"Precisión del modelo: {accuracy * 100:.2f}%")

# Prueba
predicciones = model.predict(X)
for i, pred in enumerate(predicciones):
    clase = np.argmax(pred)
    simbolo = ["+", "-", "="][clase]
    print(f"Entrada {i+1}: Predicción → {simbolo} (Probabilidades: {pred})")


# Prueba con entrada del usuario
def bitmap_to_array(symbol):
    if symbol == "+":
        return np.array([[0, 1, 0, 1, 1, 1, 0, 1, 0]])
    elif symbol == "-":
        return np.array([[0, 0, 0, 1, 1, 1, 0, 0, 0]])
    elif symbol == "=":
        return np.array([[1, 1, 1, 0, 0, 0, 1, 1, 1]])
    else:
        return None

simbolo_input = input("Ingrese un símbolo (+, - o =): ")
entrada = bitmap_to_array(simbolo_input)

if entrada is not None:
    prediccion = model.predict(entrada, verbose=0)
    clase = np.argmax(prediccion[0])
    simbolo_predicho = ["+", "-", "="][clase]
    print(f"\nSímbolo ingresado: {simbolo_input}")
    print(f"El modelo lo identifica como: {simbolo_predicho}")
    print(f"Probabilidades: {prediccion[0]}")
else:
    print("Símbolo no válido. Por favor ingrese +, - o =")
