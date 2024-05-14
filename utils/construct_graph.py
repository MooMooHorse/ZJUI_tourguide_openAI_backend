import numpy as np

# Initialize an adjacency matrix for 9 nodes (0 to 8)
n = 9
adjacency_matrix = np.zeros((n, n), dtype=int)

# List of edges, each tuple is an edge and each edge is bidirectional
edges = [(0, 1), (1, 8), (8, 6), (6, 7), (7, 5), (5, 6), (4, 5), (4, 3), (3, 2)]

# Populate the adjacency matrix for each edge, bidirectionally
for u, v in edges:
    adjacency_matrix[u, v] = 1
    adjacency_matrix[v, u] = 1  # Since the edges are bidirectional

print(adjacency_matrix)
