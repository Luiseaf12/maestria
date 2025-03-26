import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo dirigido con pesos
G = nx.DiGraph()

# Añadir nodos y aristas con costos
edges = [
    ("A", "B", 4), ("A", "C", 2),
    ("B", "C", 5), ("B", "D", 10),
    ("C", "D", 3), ("D", "E", 8),
    ("E", "F", 4), ("C", "F", 15),
    ("B", "E", 7), ("F", "G", 6),
    ("E", "G", 5), ("D", "G", 10)
]

G.add_weighted_edges_from(edges)

# Aplicar el algoritmo A* para encontrar la ruta más corta desde A hasta G
shortest_path = nx.astar_path(G, "A", "G", weight="weight")
shortest_path_length = nx.astar_path_length(G, "A", "G", weight="weight")

# Dibujar el grafo
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=10)
edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Resaltar la ruta óptima encontrada por A*
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2)

plt.title(f"Camino más corto de A a G usando A*\nDistancia Total: {shortest_path_length}")
plt.show()

# Mostrar la ruta encontrada
shortest_path, shortest_path_length
