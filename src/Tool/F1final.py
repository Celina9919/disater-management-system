import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq  # Importing heapq for the Min-Heap implementation

"""
Prim's Algorithm is a greedy algorithm used to find the Minimum Spanning Tree (MST) of a weighted, connected, and undirected graph. 
It starts from an arbitrary node and grows the MST by incrementally adding the smallest edge that connects a node in the MST to a node outside of it. 
The process is repeated until all nodes are included, ensuring the minimum weight sum for the spanning tree
"""

# Data structure: Min-Heap (Priority Queue)
# A Min-Heap is a complete binary tree where the value at each parent node is smaller than or equal to the values of its child nodes.
# Prim's Algorithm utilizes this data structure to efficiently select the smallest edge from the priority queue, ensuring optimal performance.
# This optimization reduces the time complexity of Prim's Algorithm to O(E log V), similar to Kruskal's algorithm when sorting edges.
# By using the Min-Heap, Prim's Algorithm efficiently finds the smallest edge that connects the MST to a vertex outside the MST.

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

# Create undirected graph using NetworkX
G = nx.Graph()

# Add edges and weights to the graph from the adjacency matrix
# We iterate over the matrix to add each edge if the weight is greater than zero and it is not a self-loop (i != j).
# Self-loops (edges from a node to itself) are ignored to avoid redundant connections in the graph.
for i, row in adjacency_matrix.iterrows():
    for j, weight in row.items():
        if weight > 0 and i != j:  # Ignore zero weights and self-loops
            G.add_edge(i, j, weight=weight) # Add edge with weight if the weight is positive and it's not a self-loop

# Adding attributes to nodes to describe their locations (e.g., Hospital, Rescue Station)
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

# Set the node attributes using the description for each node
nx.set_node_attributes(G, node_attributes, "description")

# Adding attributes to edges
# If an edge connects 'E' (Boat Rescue) and 'I' (Staging Area), mark it as a "Waterway" and color it blue to highlight the special nature of this connection.
# Other edges are colored light gray and have no specific type assigned.
for u, v in G.edges():
    if ('E' in {u, v}) and ('I' in {u, v}): # Check if the edge connects E and I
        G.edges[u, v]["type"] = "Waterway"
        G.edges[u, v]["color"] = "blue"
    else:
        G.edges[u, v]["color"] = "lightgray" # Color normal edges light gray
        G.edges[u, v]["type"] = " "          # No specific type for other edges

# Function to implement Prim's Algorithm using Min-Heap for (MST)
# The algorithm starts from the specified start_node and progressively adds the smallest edge to the MST.
# A priority queue (Min-Heap) is used to always select the smallest edge that connects the MST to an unvisited node.
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
    mst_edges = []  # List to store the edges that make up the MST
    visited = set()  # Set to track visited nodes
    min_heap = []  # Min-Heap (priority queue) to store edges (weight, node(start_node), neighbor)

    # Mark the start node as visited and add its edges to the heap
    visited.add(start_node)                      # Mark the start node as visited
    for neighbor, data in G[start_node].items(): # Add edges of the start node to the Min-Heap
        heapq.heappush(min_heap, (data['weight'], start_node, neighbor)) # Push edges of the start node to the Min-Heap

    # Run Prim's algorithm : Extract edges from the Min-Heap and add them to the MST
    while min_heap:
        weight, node, neighbor = heapq.heappop(min_heap) # Get the edge with the smallest weight and Pop the smallest edge from the heap

        # If the neighbor node has not been visited yet, add it to the MST
        if neighbor not in visited:
            visited.add(neighbor) # Mark the neighbor as visited
            mst_edges.append((node, neighbor, weight)) # Add the edge to the MST

            # Add all edges of the newly added node to the Min-Heap for future consideration
            # This step ensures that we evaluate all possible edges connecting the new node to any other unvisited nodes.
            for next_neighbor, data in G[neighbor].items():
                if next_neighbor not in visited:
                    heapq.heappush(min_heap, (data['weight'], neighbor, next_neighbor)) # Push edge to the heap

    # Calculate the total weight (cost) of the MST
    # This step sums up the weights of all edges in the MST to determine the total cost of constructing the minimum spanning tree.
    total_cost = sum(weight for _, _, weight in mst_edges)

    return mst_edges, total_cost

# Run Prim's algorithm starting from node 'A'
start_node = 'A'
mst_edges, minimum_cost = prim_algorithm(G, start_node)

# Print the total minimum cost of the MST (rebuilding infrastructure)
print(f"The minimum cost to rebuild the infrastructure of Schilda city is: {minimum_cost}")

# Create the MST graph
mst = nx.Graph()
mst.add_weighted_edges_from(mst_edges)

# Generate labels for nodes to include their descriptions
node_labels = {node: f"{node}: {data['description']}" for node, data in G.nodes(data=True)}

# Generate labels for edges to show their type and weight
edge_labels = {(u, v): f"{data['type']} ({data.get('weight', 0)})" for u, v, data in G.edges(data=True)}

# Visualization of the graph and MST
pos = nx.spring_layout(G, seed=42)  # Layout for consistent node placement across runs
plt.figure(figsize=(12, 12)) # Set the figure size for better readability

# Draw all nodes in the graph with a specific color and size
nx.draw_networkx_nodes(G, pos, node_size=700, node_color="rosybrown")

# Draw node labels with descriptions
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_color="navy", font_weight="bold", font_family="monospace")

# Draw all edges with their respective colors (light gray for normal, blue for waterways)
edge_colors = [data["color"] for _, _, data in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1)

# Draw MST edges on top to highlight them in red
nx.draw_networkx_edges(mst, pos, edge_color="red", width=3)

# Add edge labels for the attributes such as type and weight
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, font_color="black", font_family="monospace")

# Set the title for the plot
plt.title("Minimum Cost of Rebuilding Infrastructure of Schilda City")
plt.show()

"""
Time Complexity of Prim's Algorithm:
    - Min Heap Operations: Each edge is pushed or updated in the priority queue once, which takes  O(ElogV) time in total.
    - Vertex Processing: Each vertex is extracted from the queue once,  and since the graph is connected, we process each vertex once, taking O(VlogV) time.
    - Overall Complexity: O(ElogV+VlogV)
As E>V in a complete graphs, the overall complexity simplifies to: O(ElogV)
In this case, for the given graph with 9 nodes (V=9), and 36 edges (E=36) in a Complete graph <= (9*(9-1))/2 = 36.
Complexity: O(36log9)=O(36*3)=O(108)

"""

#References: https://www.geeksforgeeks.org/difference-between-prims-and-kruskals-algorithm-for-mst/ this our code for function 1: F1: Rebuilding the communication infrastructure