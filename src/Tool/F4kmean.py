"""
Using K-Means Clustering Algorithm to add 2 additional supply points
K-Means Clustering → Iterative partitioning of nodes.
Dijkstra's Algorithm → For distance calculations.

"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
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

# Add node descriptions
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
nx.set_node_attributes(G, node_attributes, 'description')

# K-Means Clustering Algorithm
# Step 1: Initialize Random Centroids
def initialize_centroids(nodes, k):
    return random.sample(nodes, k) # Randomly selects k initial centroids.

# Step 2: Assign Nodes to Nearest Centroid
# Assigns each node to the closest centroid using the shortest path.

def assign_clusters(graph, centroids):
    clusters = {centroid: [] for centroid in centroids}
    for node in graph.nodes():
        if node not in centroids:
            distances = [nx.shortest_path_length(graph, node, centroid, weight='weight') for centroid in centroids]
            closest_centroid = centroids[distances.index(min(distances))]
            clusters[closest_centroid].append(node)
    return clusters

#Step 3: Update Centroids. Updates centroids by finding the node with the minimum average distance to others.
def update_centroids(graph, clusters):
    new_centroids = []
    for nodes in clusters.values():
        min_total_distance = float('inf')
        best_node = None
        for node in nodes:
            total_distance = sum(nx.shortest_path_length(graph, node, other, weight='weight') for other in nodes)
            if total_distance < min_total_distance:
                min_total_distance = total_distance
                best_node = node
        new_centroids.append(best_node)
    return new_centroids

# Step 4: Run K-Means Iteratively
def k_means(graph, k=2, max_iter=10):
    nodes = list(graph.nodes())
    centroids = initialize_centroids(nodes, k)
    for _ in range(max_iter):
        clusters = assign_clusters(graph, centroids)
        new_centroids = update_centroids(graph, clusters)
        if new_centroids == centroids:
            break
        centroids = new_centroids
    return clusters

# Apply K-Means Clustering
clusters = k_means(G, k=2)

# Add supply points J and K with dynamic edge weights
supply_points = ['J', 'K']
for supply_point, (centroid, nodes) in zip(supply_points, clusters.items()):
    G.add_node(supply_point, description='Supply Point')
    for node in nodes:
        try:
            # Use the actual shortest path distance to G and reduce it by 10% to prioritize J/K
            distance_to_G = nx.shortest_path_length(G, source=node, target='G', weight='weight')
            optimized_weight = max(1, int(distance_to_G * 0.9))
        except nx.NetworkXNoPath:
            optimized_weight = 1  # Default weight if no path is found
        G.add_edge(supply_point, node, weight=optimized_weight, color='green')

# Display distances from J and K to their grouped nodes
for supply_point, (centroid, nodes) in zip(supply_points, clusters.items()):
    print(f"Distances from {supply_point} to its clustered nodes:")
    for node in nodes:
        try:
            distance = nx.shortest_path_length(G, source=supply_point, target=node, weight='weight')
            print(f"  {supply_point} -> {node}: {distance}")
        except nx.NetworkXNoPath:
            print(f"  {supply_point} -> {node}: No path found")

# Visualization
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(10, 10))
node_colors = ["yellow" if node in ['J', 'K'] else "rosybrown" for node in G.nodes]
nx.draw_networkx_nodes(G, pos, node_size=800, node_color=node_colors)
nx.draw_networkx_labels(G, pos, labels={node: f"{node}: {data.get('description', '')}" for node, data in G.nodes(data=True)}, font_size=8, font_color="navy")

edge_colors = [data.get("color", "lightgray") for _, _, data in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1.5)

edge_labels = {(u, v): f"{int(d['weight'])}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=8)

plt.title("Graph with K-Means Clustering Supply Points (J, K)")
plt.show()
