from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd


# Crear un conjunto de datos de compras de clientes
data = {
    'Pan': [1, 0, 1, 1, 0, 1],
    'Leche': [1, 1, 1, 0, 1, 1],
    'Mantequilla': [0, 1, 1, 1, 1, 0],
    'Cereal': [0, 1, 0, 1, 1, 1],
    'Queso': [1, 0, 1, 0, 0, 1]
}

# Convertir a DataFrame
df = pd.DataFrame(data)

# Aplicar el algoritmo A PRIORI
frequent_itemsets = apriori(df, min_support=0.5, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

# Mostrar resultados
print("\nConjuntos de items frecuentes:")
print("-" * 50)
print(frequent_itemsets)

print("\nReglas de asociación generadas:")
print("-" * 50)
print(rules)
