"""
In the first functions, there are two ways to calculate the minimum rebuilding cost for Schilda city: Prim Algorithm and Kruskal Algorithm.
Both of them work with MST - Minimum Spanning Tree, which is a subgraph of a graph that satisfies specific properties.
At the end,  both algorithms deliver the same minimum cost to rebuild the infrastructure of Schilda city.
Prim Algorithm is served for the dense graph whereas the Kruskal Algorithm is for the sparse graph. However, in this case, the data used is a dense graph.
Hence, the Prim Algorithm is the most appropriate algorithm for this case.
Infrastructure of Schilda City:
- A: Hospital
- B: Rescue Station
- C: Government Building
- D: Evacuation Point to gather people
- E: Boat Rescue
- F: Emergency Service
- G: Supply Point
- H, I: Staging Area
- EI: Waterway
"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

"""
Prim's Algorithm is a greedy algorithm used to find the Minimum Spanning Tree (MST) of a weighted, connected, and undirected graph.
It grows the MST incrementally by adding the smallest edge that connects a vertex in the MST to a vertex outside the MST.
"""

# Data structure: Min Heap which makes the Prim Algorithm more optimized and the time complexity similar to the one of Kruskal Algorithm as it is used to efficiently find the smallest edge connecting the MST to a vertex outside the MST.
# A Min Heap is a complete binary tree in which the value in each internal node is smaller than or equal to the values in the children of that node.

# Load the adjacency matrix from the provided file
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
    if ('E' in {u, v}) and ('I' in {u, v}):
        G.edges[u, v]["type"] = "Waterway"
        G.edges[u, v]["color"] = "blue"
    else:
        G.edges[u, v]["color"] = "lightgray"
        G.edges[u, v]["type"] = " "

# Use Prim's algorithm to find the MST
# The Min-Heap is not explicitly coded in the provided exercise because the NetworkX library abstracts the implementation of Prim's Algorithm, including the use of a Min-Heap.
mst = nx.minimum_spanning_tree(G, algorithm="prim")

# Calculate the total weight (minimum cost) of the MST
minimum_cost = sum(d['weight'] for _, _, d in mst.edges(data=True))

"""
mst.edges(data=True):

- This retrieves all the edges of the graph mst (which is the MST computed earlier) as a generator.
- Each edge is represented as a tuple (u,v,d), where:
    --u: The source node.
    --v: The destination node.
    --d: A dictionary of edge attributes (e.g., weights).
"""

print(f"The minimum cost to rebuild the infrastructure of Schilda city is: {minimum_cost}")

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

#References: https://www.geeksforgeeks.org/difference-between-prims-and-kruskals-algorithm-for-mst/