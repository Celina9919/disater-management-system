import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

# Load the adjacency matrix
file_path = 'src/Data/undirected_weighted_graph.txt'
adjacency_matrix = pd.read_csv(file_path, delim_whitespace=True, index_col=0)

# Create a graph from the adjacency matrix
G = nx.Graph()

for i, row in adjacency_matrix.iterrows():
    for j, weight in row.items():
        if weight > 0 and i != j:
            G.add_edge(i, j, weight=weight)

# Adding attributes to nodes
node_attributes = {
    'A': "Hospital",
    'B': "Rescue Station",
    'C': "Government Building",
    'D': "Evacuation Point",
    'E': "Boat Rescue",
    'F': "Emergency Service",
    'G': "Supply Point",
    'H': "Staging Area",
    'I': "Staging Area"
}
nx.set_node_attributes(G, node_attributes, "description")

# K-Medoid Algorithm Implementation
def k_medoid(graph, k=3, max_iter=100):
    nodes = list(graph.nodes)
    medoids = random.sample(nodes, k)

    for _ in range(max_iter):
        clusters = {medoid: [] for medoid in medoids}
        
        # Assignment step: assign each node to the closest medoid
        for node in nodes:
            distances = [nx.shortest_path_length(graph, source=node, target=medoid, weight='weight') for medoid in medoids]
            closest_medoid = medoids[np.argmin(distances)]
            clusters[closest_medoid].append(node)
        
        # Update step: choose a new medoid that minimizes the total distance within each cluster
        new_medoids = []
        for medoid, cluster_nodes in clusters.items():
            min_total_distance = float('inf')
            best_candidate = medoid
            for candidate in cluster_nodes:
                total_distance = sum(nx.shortest_path_length(graph, source=candidate, target=other, weight='weight') for other in cluster_nodes)
                if total_distance < min_total_distance:
                    min_total_distance = total_distance
                    best_candidate = candidate
            new_medoids.append(best_candidate)
        
        # Check for convergence
        if set(new_medoids) == set(medoids):
            break
        medoids = new_medoids

    return medoids

# Run K-Medoid Algorithm with G fixed as an initial supply point
medoids = k_medoid(G, k=3)
medoids.remove('G')  # Keep G fixed, select the other two for J and K

# Add new supply points J and K connected optimally
new_supply_nodes = ['J', 'K']
for i, medoid in enumerate(medoids):
    G.add_node(new_supply_nodes[i], description='Supply Point')
    G.add_edge(new_supply_nodes[i], medoid, weight=2)  # Connect directly to the medoid
    # Also connect to the nearest neighbor of the medoid for better integration
    closest_neighbor = min(
        [n for n in G.nodes if n not in new_supply_nodes + ['G']],
        key=lambda n: nx.shortest_path_length(G, source=medoid, target=n, weight='weight')
    )
    G.add_edge(new_supply_nodes[i], closest_neighbor, weight=2)

# Visualization
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(10, 10))

node_colors = ["orange" if n in new_supply_nodes + ['G'] else "rosybrown" for n in G.nodes]
nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors)
nx.draw_networkx_labels(G, pos, labels={node: f"{node}: {data['description']}" for node, data in G.nodes(data=True)}, font_size=8, font_color="navy", font_weight="bold")

# Draw edges with weights
nx.draw_networkx_edges(G, pos, edge_color="lightgray", width=1)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=8)

plt.title("Supply Points Positioned Using K-Medoid Algorithm")
plt.show()