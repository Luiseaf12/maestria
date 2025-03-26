from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Generar datos simulados con 3 grupos
np.random.seed(42)
grupo1 = np.random.normal(loc=[2, 2], scale=0.5, size=(50, 2))
grupo2 = np.random.normal(loc=[6, 6], scale=0.5, size=(50, 2))
grupo3 = np.random.normal(loc=[10, 2], scale=0.5, size=(50, 2))

# Combinar los grupos en un solo dataset
data = np.vstack((grupo1, grupo2, grupo3))
df = pd.DataFrame(data, columns=['X', 'Y'])

# Aplicar K-Means con 3 clústeres
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(df[['X', 'Y']])

# Mostrar DataFrame con etiquetas de clústeres
print("\nResultados de Clustering con K-Means:")
print("-" * 50)
print(df)

# Visualizar los clústeres
plt.figure(figsize=(8, 6))
plt.scatter(df['X'], df['Y'], c=df['Cluster'], cmap='viridis', edgecolors='k', alpha=0.7)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', marker='X', s=200, label='Centroides')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Clustering de Datos con K-Means')
plt.legend()
plt.show()
