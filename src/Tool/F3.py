"""
    Chose the scene of the emergency service (Node F) can only be reached by the fastest hybrid route (car + boat) from other places.
    Target Node: F (Emergency Service)
    Stop Node: E (Boat Rescue) and I (Staging Area) but edge EI cannot be separated as it is the waterway
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the adjacency matrix
file_path = 'src/Data/undirected_weighted_graph.txt'
adjacency_matrix = pd.read_csv(file_path, delim_whitespace=True, index_col=0)

# Create a graph from the adjacency matrix
G = nx.Graph()

# Add edges and weights to the graph
for i, row in adjacency_matrix.iterrows():
    for j, weight in row.items():
        if weight > 0 and i != j:  # Ignore zero weights and self-loops
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

# Adding attributes to edges
for u, v in G.edges():
    if {'E', 'I'} <= {u, v}:  # Check if the edge is between E and I
        G.edges[u, v]["type"] = "Waterway"
        G.edges[u, v]["color"] = "blue"
    else:
        G.edges[u, v]["color"] = "lightgray"
        G.edges[u, v]["type"] = " "

# Navigation system: Calculate the fastest route through E-I (inseparable waterway)
def calculate_distances_via_ei(graph, ei_nodes, target_node):
    distances = {}
    paths = {}
    e_node, i_node = ei_nodes

    for node in graph.nodes:
        if node != target_node and node != e_node and node != i_node:
            try:
                # Path through inseparable E-I waterway
                path_to_e = nx.dijkstra_path(graph, source=node, target=e_node, weight='weight')
                path_e_to_i = nx.dijkstra_path(graph, source=e_node, target=i_node, weight='weight')
                path_i_to_target = nx.dijkstra_path(graph, source=i_node, target=target_node, weight='weight')

                # Combine paths
                full_path = path_to_e[:-1] + path_e_to_i[:-1] + path_i_to_target
                total_distance = (
                    nx.dijkstra_path_length(graph, source=node, target=e_node, weight='weight') +
                    nx.dijkstra_path_length(graph, source=e_node, target=i_node, weight='weight') +
                    nx.dijkstra_path_length(graph, source=i_node, target=target_node, weight='weight')
                )
            except nx.NetworkXNoPath:
                full_path, total_distance = None, float('inf')

            paths[node] = full_path
            distances[node] = total_distance

    # Print distances and paths
    print(f"Distances and paths to {target_node} via inseparable E-I waterway:")
    for node, distance in distances.items():
        if paths[node]:
            print(f"From {node} to {target_node}: Distance = {distance}, Path = {paths[node]}")
        else:
            print(f"No path from {node} to {target_node}")

    return paths, distances

# Nodes for inseparable waterway and target
ei_nodes = ('E', 'I')
target_node = 'F'

# Calculate distances and paths to the target node
paths_to_target, distances_to_target = calculate_distances_via_ei(G, ei_nodes, target_node)

# Visualization
pos = nx.spring_layout(G, seed=42)  # Layout for consistent visualization
plt.figure(figsize=(12, 12))

# Draw all nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color="rosybrown")
nx.draw_networkx_labels(G, pos, labels={node: f"{node}: {data['description']}" for node, data in G.nodes(data=True)},
                        font_size=8, font_color="navy", font_weight="bold", font_family="monospace")

# Draw all edges with their respective colors
edge_colors = [data["color"] for _, _, data in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1)

# Highlight paths to the target node
for node, path in paths_to_target.items():
    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="olivedrab", width=2.5)

# Add edge labels for the attributes
edge_labels = {(u, v): f"{data['type']} ({data.get('weight', 0)})" for u, v, data in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, font_color="black", font_family="monospace")

plt.title(f"Fastest Routes to Target Node '{target_node}: Emergency Service' via inseparable E-I")
plt.show()




"""
# Algorithm Used: Dijkstra's Algorithm to calculate the shortest paths in a graph.
## This function is split into two steps for each node:
### Shortest Path from the Node to E (Stop Node): Uses Dijkstra's algorithm to compute the shortest path from the current node to E.
### Shortest Path from the Node E to I (Stop Node): Uses Dijkstra's algorithm to compute the shortest path from the current node to E.
### Shortest Path from I to F (Target Node):  Uses Dijkstra's algorithm to compute the shortest path from E to F.
The paths and distances are then combined to calculate the overall shortest hybrid route for each node to the target node.

# Data Structure Used:
## Graph Representation: The graph is represented using an Adjacency List provided by NetworkX.
## Priority Queue (Min-Heap): Dijkstra's algorithm uses a min-heap to efficiently retrieve the next closest node. It is implemented internally by NetworkX.

#Time Complexity:
- Priority Queue Operations: Each operation (insert, extract-min) takes O(logV).
=> Each node (except E, I and F) executes these operations twice, resulting in O(V⋅(V+E)logV) = O(9 * (9+36) * log9) = O(9 * 45 * 3) = O(1215)
"""

