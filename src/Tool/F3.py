"""
    Chose the scene of the emergency service (Node F) can only be reached by the fastest hybrid route (car + boat) from other places.
    Target Node: F (Emergency Service)
    Stop Node: E (Boat Rescue) and I (Staging Area) but edge EI cannot be separated as it is the waterway
"""
import pandas as pd # Used for handling and loading the adjacency matrix from a text file.
import networkx as nx # Used to create and manipulate the graph.
import matplotlib.pyplot as plt # Used to visualize the graph.
import heapq # Provides a priority queue (for Dijkstra's algorithm optimization).

# Load the adjacency matrix
file_path = 'src/Data/undirected_weighted_graph.txt' # Path to the adjacency matrix file.
adjacency_matrix = pd.read_csv(file_path, delim_whitespace=True, index_col=0) # Reads the adjacency matrix into a DataFrame.

# Create a graph from the adjacency matrix
G = nx.Graph() # Initializes an undirected weighted graph using NetworkX.

# Add edges and weights to the graph
# Iterates through the matrix and adds edges between nodes with weights > 0, ignoring self-loops (i != j).
# i != j: This is the key condition that ignores self-loops.
# A self-loop occurs when a node has an edge to itself, meaning i == j.
# By checking i != j, the code explicitly skips adding edges where the source node and the target node are the same.
for i, row in adjacency_matrix.iterrows():
    # adjacency_matrix.iterrows() iterates over the rows of the adjacency matrix, where i is the index of the current row (representing a node), and row contains the connection weights to other nodes.
    for j, weight in row.items(): # row.items() iterates over each column in the row, where j is the index of the column (another node), and weight is the connection weight between node i and node j
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

# Dijkstra's algorithm
def dijkstra(graph, start, target):
    # Initializes distance to all nodes as infinity, except the start node (0).
    distances = {node: float('inf') for node in graph.nodes}
    # distances: Initializes all node distances to infinity (∞) to represent that they are unreachable at first.
    # The start node's distance is set to 0 because the distance from a node to itself is zero. This allows the algorithm to later update these distances as it discovers shorter paths
    distances[start] = 0
    previous_nodes = {node: None for node in graph.nodes} # previous_nodes keeps track of the shortest path.
    # Takes O(V) time because each node is processed once
    queue = [(0, start)] # queue: A priority queue containing nodes to be explored. It starts with the start node. Takes O(1) time.
    # Total for this step: O(V)
    
    # While loop runs until all nodes have been processed. The queue is sorted by distance, and the node with the smallest distance is selected.
    while queue:
        queue.sort()
        # Sorting a list of size V takes O(V log V) in each iteration. Since this happens up to V times, it contributes O(V² log V)
        current_distance, current_node = queue.pop(0) # Popping the first element after sorting takes O(1).
        
        # Stops once the target node is reached.
        if current_node == target:
            break
        
        # Updates the distance to neighbors if a shorter path is found.
        # For each neighbor of a node, the algorithm checks if a better path exists. Each edge is checked once. It takes O(E) time across the entire run.
        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                queue.append((distance, neighbor)) # Adds neighbors to the queue. It takes O(1) time.

    # Once the loop finishes, the algorithm reconstructs the shortest path from the target back to the start using the previous_nodes dictionary.
    # This reconstruction step traces back the path, taking O(E) time.
    path = []
    current = target
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    return path, distances[target] # The function returns the final path and its total distance.

# Force all paths to go through inseparable E-I. Initializes dictionaries for storing paths and distances.
def calculate_distances_via_ei(graph, ei_nodes, target_node):
    distances = {}
    paths = {}
    e_node, i_node = ei_nodes # ei_nodes is the inseparable pair ('E', 'I').
    
    # Iterates through all nodes except the target and E/I.
    for node in graph.nodes:
        if node != target_node and node not in ei_nodes:
            # Path: source -> E -> I -> target. Forces the path to go through E → I → Target.
            path_to_e, dist_to_e = dijkstra(graph, node, e_node)
            path_i_to_target, dist_i_to_target = dijkstra(graph, i_node, target_node)
            total_dist_ei = graph[e_node][i_node]['weight']

            full_path_ei = path_to_e + [i_node] + path_i_to_target[1:]
            total_distance_ei = dist_to_e + total_dist_ei + dist_i_to_target

            # Path: source -> I -> E -> target. Forces the path to go through I → E → Target.
            path_to_i, dist_to_i = dijkstra(graph, node, i_node)
            path_e_to_target, dist_e_to_target = dijkstra(graph, e_node, target_node)

            full_path_ie = path_to_i + [e_node] + path_e_to_target[1:]
            total_distance_ie = dist_to_i + total_dist_ei + dist_e_to_target

            # Chooses the shorter path between the two E or I depending on the shorter distances from the source node to E or I
            if total_distance_ei <= total_distance_ie:
                paths[node] = full_path_ei
                distances[node] = total_distance_ei
            else:
                paths[node] = full_path_ie
                distances[node] = total_distance_ie

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
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(10, 10))

nx.draw_networkx_nodes(G, pos, node_size=700, node_color="rosybrown")
nx.draw_networkx_labels(G, pos, labels={node: f"{node}: {data['description']}" for node, data in G.nodes(data=True)},
                        font_size=8, font_color="navy", font_weight="bold")

edge_colors = [data["color"] for _, _, data in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1)


# Draw edge weights
edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}

for node, path in paths_to_target.items():
    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="olivedrab", width=2.5)
        edge_labels.update({(path[i], path[i + 1]): f"{G[path[i]][path[i + 1]]['weight']}" for i in range(len(path) - 1)})
        
edge_labels.update({(u, v): 'Waterway' for u, v in G.edges() if G.edges[u, v].get("type") == "Waterway"})

if G.has_edge('F', 'E'):
    edge_labels[('F', 'E')] = 'Impassable'
    edge_labels[('E', 'F')] = 'Impassable'

# Put edge labels to ensure highlighted paths have their weights shown
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=8)

plt.title(f"Fastest Hybrid Routes to Target Node '{target_node}: Emergency Service'")
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

Sorting: O(V² log V) (due to list sorting in the queue)
Edge Reconstruction: O(E)
Total: O(V² log V + E)
"""

