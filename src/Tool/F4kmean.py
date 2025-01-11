"""
Using K-Means Clustering Algorithm to add 2 additional supply points

"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

# Load adjacency matrix
file_path = '/mnt/data/undirected_weighted_graph.txt'  # Update to your file path
adjacency_matrix = pd.read_csv(file_path, sep='\s+', index_col=0)

# Create an undirected graph
G = nx.from_pandas_adjacency(adjacency_matrix, create_using=nx.Graph)

# Convert the undirected graph to a directed graph
city_map = nx.DiGraph()
for u, v, data in G.edges(data=True):
    city_map.add_edge(u, v, capacity=data.get("weight", adjacency_matrix.loc[u, v]))
    city_map.add_edge(v, u, capacity=data.get("weight", adjacency_matrix.loc[u, v]))

# Assign attributes to nodes
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
nx.set_node_attributes(city_map, node_attributes, "description")

# Shelter capacities
shelters = {
    'A': 200,
    'B': 150,
    'C': 250,
    'H': 50,
    'I': 50
}
nx.set_node_attributes(city_map, shelters, "capacity")

# Relief force deployment locations
deployment_locations = {
    'E': 30,  # Boat Rescue
    'F': 40,  # Emergency Service
    'G': 50,  # Supply Point
    'H': 20,  # Staging Area
    'I': 10   # Staging Area
}

# Function to determine optimal locations for supply points
def find_optimal_supply_points(graph, deployment_locations, k):
    # Extract coordinates of deployment locations
    pos = nx.spring_layout(graph, seed=42)  # Using a spring layout for coordinates
    deployment_coords = [pos[node] for node in deployment_locations.keys()]
    weights = list(deployment_locations.values())

    # Convert to numpy arrays for clustering
    deployment_coords = np.array(deployment_coords)
    weights = np.array(weights)

    # Perform weighted K-Means clustering
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(deployment_coords, sample_weight=weights)

    # Get the cluster centers (optimal supply points)
    cluster_centers = kmeans.cluster_centers_
    return cluster_centers

# Determine 2 additional supply points
additional_supply_points = find_optimal_supply_points(city_map, deployment_locations, k=2)

# Visualize the supply points
def visualize_supply_points(graph, deployment_locations, additional_points, title="Supply Points Visualization"):
    pos = nx.spring_layout(graph, seed=42)  # Generate consistent layout
    plt.figure(figsize=(12, 8))

    # Draw the original graph
    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color="rosybrown")
    nx.draw_networkx_edges(graph, pos, alpha=0.7)

    # Highlight deployment locations
    deployment_pos = {node: pos[node] for node in deployment_locations.keys()}
    nx.draw_networkx_nodes(graph, deployment_pos, node_size=800, node_color="lightblue")

    # Add additional supply points
    for point in additional_points:
        plt.scatter(point[0], point[1], color="green", s=200, label="New Supply Point")

    # Add labels
    nx.draw_networkx_labels(graph, pos, font_size=10, font_color="black")

    plt.title(title, fontsize=14)
    plt.legend()
    plt.axis("off")
    plt.show()

visualize_supply_points(city_map, deployment_locations, additional_supply_points)

# Print results
print("New Supply Points (Coordinates):")
for i, point in enumerate(additional_supply_points, start=1):
    print(f"Supply Point {i}: {point}")
