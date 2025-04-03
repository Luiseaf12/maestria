import random
import numpy as np
import matplotlib.pyplot as plt

# Crear 10 ciudades con coordenadas (x, y)
NUM_CIUDADES = 20
ciudades = np.random.rand(NUM_CIUDADES, 2)


# Calcular la distancia total de una ruta
def calcular_distancia(ruta):
    distancia = 0
    for i in range(len(ruta)):
        ciudad_actual = ciudades[ruta[i]]
        ciudad_siguiente = ciudades[ruta[(i + 1) % len(ruta)]]
        distancia += np.linalg.norm(ciudad_actual - ciudad_siguiente)
    return distancia


# Crear una ruta aleatoria
def crear_ruta():
    ruta = list(range(NUM_CIUDADES))
    random.shuffle(ruta)
    return ruta


# Selección de los mejores individuos
def seleccion(poblacion, fitness, n=2):
    return [x for _, x in sorted(zip(fitness, poblacion))][:n]


# Cruce de dos rutas (ordenado)
def cruzar(padre1, padre2):
    start, end = sorted(random.sample(range(NUM_CIUDADES), 2))
    hijo = [None] * NUM_CIUDADES
    hijo[start:end] = padre1[start:end]
    p2 = [ciudad for ciudad in padre2 if ciudad not in hijo]
    i = 0
    for j in range(NUM_CIUDADES):
        if hijo[j] is None:
            hijo[j] = p2[i]
            i += 1
    return hijo


# Mutación (intercambiar dos ciudades)
def mutar(ruta, prob=0.1):
    if random.random() < prob:
        i, j = random.sample(range(NUM_CIUDADES), 2)
        ruta[i], ruta[j] = ruta[j], ruta[i]
    return ruta


# Algoritmo genético principal
def algoritmo_genetico(generaciones=100, tam_poblacion=100):
    poblacion = [crear_ruta() for _ in range(tam_poblacion)]
    mejor_distancia = float("inf")
    mejor_ruta = None

    for gen in range(generaciones):
        fitness = [calcular_distancia(ruta) for ruta in poblacion]
        nueva_poblacion = seleccion(poblacion, fitness, n=10)

        while len(nueva_poblacion) < tam_poblacion:
            padres = random.sample(nueva_poblacion[:10], 2)
            hijo = cruzar(padres[0], padres[1])
            hijo = mutar(hijo)
            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

        # Guardar la mejor ruta encontrada
        mejor_idx = np.argmin(fitness)
        if fitness[mejor_idx] < mejor_distancia:
            mejor_distancia = fitness[mejor_idx]
            mejor_ruta = poblacion[mejor_idx]

        print(f"Generación {gen+1} - Mejor distancia: {mejor_distancia:.4f}")

    return mejor_ruta, mejor_distancia


# Ejecutar
mejor_ruta, mejor_dist = algoritmo_genetico()

# Mostrar resultado
print("\nMejor ruta encontrada:", mejor_ruta)
print("Distancia total:", mejor_dist)

# Dibujar la ruta
ruta_coords = ciudades[mejor_ruta + [mejor_ruta[0]]]
plt.plot(ruta_coords[:, 0], ruta_coords[:, 1], "o-")
plt.title("Ruta óptima encontrada")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.show()
