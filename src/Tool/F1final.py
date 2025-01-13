import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq  # Importing heapq for the Min-Heap implementation

"""
Prim's Algorithm is a greedy algorithm used to find the Minimum Spanning Tree (MST) of a weighted, connected, and undirected graph.
It grows the MST incrementally by adding the smallest edge that connects a vertex in the MST to a vertex outside the MST.
"""

# Data structure: Min Heap which makes the Prim Algorithm more optimized and the time complexity similar to the one of Kruskal Algorithm as it is used to efficiently find the smallest edge connecting the MST to a vertex outside the MST.
# A Min Heap is a complete binary tree in which the value in each internal node is smaller than or equal to the values in the children of that node.

# Function to load adjacency matrix from file
def load_adjacency_matrix(file_path):
    """
    Function to load the adjacency matrix from a file.
    
    Parameters:
        file_path (str): Path to the file containing the adjacency matrix.
        
    Returns:
        pd.DataFrame: Adjacency matrix as a pandas DataFrame.
    """
    #return pd.read_csv(file_path, delim_whitespace=True, index_col=0)
    return pd.read_csv(file_path, sep='\s+', index_col=0)  # Updated to use sep='\s+'

# Load the adjacency matrix from the file
file_path = 'src/Data/undirected_weighted_graph.txt'  # Specify the path to your file here
adjacency_matrix = load_adjacency_matrix(file_path)

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
    if ('E' in {u, v}) and ('I' in {u, v}):
        G.edges[u, v]["type"] = "Waterway"
        G.edges[u, v]["color"] = "blue"
    else:
        G.edges[u, v]["color"] = "lightgray"
        G.edges[u, v]["type"] = " "

# Function to implement Prim's Algorithm using Min-Heap
def prim_algorithm(G, start_node):
    """
    Function to implement Prim's Algorithm for Minimum Spanning Tree (MST).
    
    Parameters:
        G (networkx.Graph): The graph to compute MST for.
        start_node (str): The node to start the MST from.
        
    Returns:
        mst_edges (list): List of edges in the MST.
        total_cost (int): Total weight of the MST.
    """
    mst_edges = []  # To store the edges of the MST
    visited = set()  # To track visited nodes
    min_heap = []  # Min-Heap to store edges (weight, node, neighbor)

    visited.add(start_node)

    # Add edges of the start node to the Min-Heap
    for neighbor, data in G[start_node].items():
        heapq.heappush(min_heap, (data['weight'], start_node, neighbor))

    # Run Prim's algorithm
    while min_heap:
        weight, node, neighbor = heapq.heappop(min_heap)

        # If the neighbor node has not been visited yet, add it to the MST
        if neighbor not in visited:
            visited.add(neighbor)
            mst_edges.append((node, neighbor, weight))

            # Add the edges of the new node to the Min-Heap
            for next_neighbor, data in G[neighbor].items():
                if next_neighbor not in visited:
                    heapq.heappush(min_heap, (data['weight'], neighbor, next_neighbor))

    # Calculate the total weight (minimum cost) of the MST
    total_cost = sum(weight for _, _, weight in mst_edges)

    return mst_edges, total_cost

# Run Prim's algorithm starting from node 'A'
start_node = 'A'
mst_edges, minimum_cost = prim_algorithm(G, start_node)

print(f"The minimum cost to rebuild the infrastructure of Schilda city is: {minimum_cost}")

# Create the MST graph
mst = nx.Graph()
mst.add_weighted_edges_from(mst_edges)

# Generate labels for nodes
node_labels = {node: f"{node}: {data['description']}" for node, data in G.nodes(data=True)}

# Generate labels for edges
edge_labels = {(u, v): f"{data['type']} ({data.get('weight', 0)})" for u, v, data in G.edges(data=True)}

# Visualization
pos = nx.spring_layout(G, seed=42)  # Layout for consistent visualization
plt.figure(figsize=(12, 12))

# Draw all nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color="rosybrown")
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_color="navy", font_weight="bold", font_family="monospace")

# Draw all edges with their respective colors
edge_colors = [data["color"] for _, _, data in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1)

# Draw MST edges on top to highlight them
nx.draw_networkx_edges(mst, pos, edge_color="red", width=3)

# Add edge labels for the attributes
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, font_color="black", font_family="monospace")

plt.title("Minimum Cost of Rebuilding Infrastructure of Schilda City")
plt.show()

"""
Overall Complexity
    - Min Heap Operations: Each edge is pushed or updated in the priority queue once: O(ElogV).
    - Vertex Processing: Each vertex is extracted from the queue once: O(VlogV).
=> Total Complexity: O(ElogV+VlogV)
As E>V in complete graphs, the overall complexity simplifies to: O(ElogV)
In this case, V=9, E=36 (Complete graph) <= (9*(9-1))/2 = 36.
Complexity: O(36log9)=O(36*3)=O(108)
"""

#References: https://www.geeksforgeeks.org/difference-between-prims-and-kruskals-algorithm-for-mst/ this our code for function 1: F1: Rebuilding the communication infrastructure
