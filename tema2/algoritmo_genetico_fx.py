import numpy as np
import matplotlib.pyplot as plt


# Función objetivo
def f(x):
    return x * np.sin(10 * np.pi * x) + 1


# Crear un individuo aleatorio
def create_individual():
    return np.random.uniform(-1, 2)


# Crear una población
def create_population(size):
    return [create_individual() for _ in range(size)]


# Selección de padres
def select_parents(population, fitness, num_parents):
    sorted_indices = np.argsort(fitness)[::-1]
    return [population[i] for i in sorted_indices[:num_parents]]


# Cruce: promedio de dos padres
def crossover(parent1, parent2):
    alpha = np.random.rand()
    return alpha * parent1 + (1 - alpha) * parent2


# Mutación: agregar ruido pequeño
def mutate(individual, mutation_rate=0.1):
    if np.random.rand() < mutation_rate:
        return individual + np.random.normal(0, 0.1)
    return individual


# Parámetros
pop_size = 20
generations = 50
mutation_rate = 0.1

# Inicializar población
population = create_population(pop_size)

for generation in range(generations):
    # Evaluar fitness
    fitness = [f(ind) for ind in population]

    # Seleccionar padres
    parents = select_parents(population, fitness, num_parents=10)

    # Crear nueva población
    new_population = []
    while len(new_population) < pop_size:
        p1, p2 = np.random.choice(parents, 2)
        child = crossover(p1, p2)
        child = mutate(child, mutation_rate)
        # Limitar al dominio [-1, 2]
        child = np.clip(child, -1, 2)
        new_population.append(child)

    population = new_population

# Mostrar mejor solución
best_individual = max(population, key=f)
print("Mejor solución:", best_individual)
print("Valor de f(x):", f(best_individual))

# Visualización
x_vals = np.linspace(-1, 2, 400)
y_vals = f(x_vals)
plt.plot(x_vals, y_vals, label="f(x)")
plt.axvline(best_individual, color="r", linestyle="--", label="Mejor solución")
plt.legend()
plt.title("Optimización con Algoritmo Genético")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.show()
