import numpy as np

# Ampliar los datos de entrada (tamaño y color) y las salidas esperadas
X = np.array(
    [
        [1, 1],  # Pan Integral: Tamaño 1, Color 1 (oscuro)
        [2, 3],  # Pan Blanco: Tamaño 2, Color 3 (claro)
        [1, 2],  # Pan Integral: Tamaño 1, Color 2
        [2, 2],  # Pan Blanco: Tamaño 2, Color 2
        [1, 1],  # Pan Integral: Tamaño 1, Color 1 (oscuro)
        [2, 3],  # Pan Blanco: Tamaño 2, Color 3 (claro)
        [1, 3],  # Pan Blanco: Tamaño 1, Color 3
        [2, 1],  # Pan Integral: Tamaño 2, Color 1
        [1, 2],  # Pan Integral: Tamaño 1, Color 2
        [2, 2],  # Pan Blanco: Tamaño 2, Color 2
        [3, 3],  # Pan Blanco: Tamaño 3, Color 3
        [3, 1],  # Pan Integral: Tamaño 3, Color 1
        [3, 2],  # Pan Blanco: Tamaño 3, Color 2
    ]
)

y = np.array([-1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1])  # Salidas esperadas

# Inicializar los pesos aleatorios y el umbral (bias)
np.random.seed(42)  # Para resultados consistentes
w = np.random.rand(2)  # Pesos para Tamaño y Color
b = np.random.rand()  # Umbral (bias)

# Definir la tasa de aprendizaje
learning_rate = 0.1


# Función de activación (signo)
def step_function(x):
    return 1 if x >= 0 else -1


# Entrenamiento del perceptrón
def train_perceptron(X, y, w, b, learning_rate, epochs):
    for epoch in range(epochs):
        for i in range(len(X)):
            # Calcular la salida del perceptrón
            linear_output = np.dot(X[i], w) + b
            output = step_function(linear_output)

            # Calcular el error
            error = y[i] - output

            # Actualizar los pesos y el umbral
            w += learning_rate * error * X[i]
            b += learning_rate * error
        # print(f"Epoch {epoch+1}: Pesos = {w}, Umbral = {b}")
    return w, b


# Entrenamos el perceptrón con 10 épocas
w, b = train_perceptron(X, y, w, b, learning_rate, epochs=10)


# Probar el perceptrón con algunos ejemplos nuevos
def predict(X, w, b):
    predictions = []
    for x in X:
        linear_output = np.dot(x, w) + b
        predictions.append(step_function(linear_output))
    return predictions


# Solicitar datos al usuario
def solicitar_datos():
    try:
        tamaño = float(input("Ingrese el tamaño del pan: "))
        color = float(input("Ingrese el color del pan (1: oscuro, 3: claro): "))
        return np.array([tamaño, color])
    except ValueError:
        print("Entrada inválida. Por favor, ingrese valores numéricos.")
        return solicitar_datos()


# Obtener datos del usuario y predecir
nuevo_pan = solicitar_datos()
prediccion = predict([nuevo_pan], w, b)[0]
tipo_pan = "Pan Blanco" if prediccion == 1 else "Pan Integral"
print(f"El pan ingresado es: {tipo_pan}")
