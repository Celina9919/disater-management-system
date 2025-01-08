"""
Use Maximum Flow Algorithms (specifically, the Edmonds-Karp Algorithm,
Edmonds-Karp algorithm uses Breadth First Search (BFS) to find augmented paths to increase flow) to determine
whether the existing infrastructure can handle the evacuation demand
from assembly points to emergency shelters, considering road and water routes.

The Edmonds-Karp algorithm works by using Breadth-First Search (BFS)
to find a path with available capacity from the source to the sink (called an augmented path),
and then sends as much flow as possible through that path.

The Edmonds-Karp algorithm continues to find new paths to send more flow through until the maximum flow is reached.
In this case:
Souce Point: Node D - Evacuation Point
Sink Points: Nodes A, B, C, H, I - Shelters

"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load adjacency matrix
file_path = 'src/Data/undirected_weighted_graph.txt'
adjacency_matrix = pd.read_csv(file_path, sep='\s+', index_col=0)

# Create an undirected graph
G = nx.from_pandas_adjacency(adjacency_matrix, create_using=nx.Graph)

# Convert the undirected graph to a directed graph
city_map = nx.DiGraph()
for u, v, data in G.edges(data=True):
    city_map.add_edge(u, v, capacity=data['weight'])
    city_map.add_edge(v, u, capacity=data['weight'])

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
    'A': 200,  # Hospital
    'B': 150,  # Rescue Station
    'C': 250,  # Government Building
    'H': 50,   # Staging Area
    'I': 50    # Staging Area
}

# Add shelter capacities as node attributes
nx.set_node_attributes(city_map, shelters, "capacity")

# Evacuation needs (source is 'D')
evacuation_needs = 300

# Add routes capacities from the source (D) to the shelters
routes = {
    ('D', 'A'): 150,
    ('D', 'B'): 130,
    ('D', 'C'): 200,
    ('D', 'H'): 20,
    ('D', 'I'): 20
}
for (start, end), capacity in routes.items():
    city_map.add_edge(start, end, capacity=capacity)

# Remove outgoing edges from shelters to enforce sink behavior
for shelter in shelters:
    city_map.remove_edges_from([(shelter, neighbor) for neighbor in city_map.successors(shelter)])

# Initialize variables
shelter_flow_details = {}
total_flow = 0

# Calculate maximum flow for each shelter independently, prioritizing smaller shelters
for shelter, capacity in sorted(shelters.items(), key=lambda x: x[1]):  # Sort by shelter capacity (ascending)
    # Calculate maximum flow from the source (D) to the shelter
    flow_value, current_flow = nx.maximum_flow(city_map, 'D', shelter, flow_func=nx.algorithms.flow.edmonds_karp)

    # Limit flow by shelter capacity
    flow_value = min(flow_value, capacity)

    # Update total flow
    total_flow += flow_value

    # Store flow details for the current shelter
    shelter_flow_details[shelter] = {}
    for u in current_flow:
        for v, flow in current_flow[u].items():
            if flow > 0:
                if u not in shelter_flow_details[shelter]:
                    shelter_flow_details[shelter][u] = {}
                shelter_flow_details[shelter][u][v] = flow

    # Reduce capacities of edges used in the flow
    for u, v, data in city_map.edges(data=True):
        if u in current_flow and v in current_flow[u]:
            data['capacity'] -= current_flow[u][v]

# Output results
print(f"Maximum Flow: {total_flow}")
print("\nFlow Details by Shelter:")
for shelter, flows in shelter_flow_details.items():
    print(f"\nShelter {shelter}:")
    if flows:
        for source, targets in flows.items():
            for target, flow in targets.items():
                print(f"  {source} -> {target}: {flow}")
    else:
        print("  No flow received.")

# Visualization
def visualize_evacuation_flow(graph, flow_dict, title="Evacuation Flow Visualization"):
    pos = nx.spring_layout(graph, seed=42, k=3)
    plt.figure(figsize=(12, 8))

    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color="rosybrown")

    edge_colors = []
    for u, v, data in graph.edges(data=True):
        edge_colors.append("gray")

    nx.draw_networkx_edges(graph, pos, width=2, alpha=0.7, edge_color=edge_colors)

    # Add capacity information to node labels
    node_labels = {}
    for node, data in graph.nodes(data=True):
        description = data.get('description', 'No description')
        capacity = data.get('capacity', None)
        if capacity:
            node_labels[node] = f"{node}: {description}\n{capacity}"
        else:
            node_labels[node] = f"{node}: {description}"

    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=10, font_color="black")

    # Add flow information to edge labels
    edge_labels = {}
    for shelter, flows in shelter_flow_details.items():
        for source, targets in flows.items():
            for target, flow in targets.items():
                edge_labels[(source, target)] = f"{flow}"
    
    # Decision
        if total_flow >= evacuation_needs:
            print("\nThe existing infrastructure is sufficient for evacuation.")
        else:
            print("\nAdditional infrastructure is needed for evacuation.")

    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="blue", font_size=8)
    plt.title(title, fontsize=14)
    plt.axis("off")
    plt.show()

visualize_evacuation_flow(city_map, shelter_flow_details)

"""
Output Explaination:
Shelter A: 150 people
Shelter B: 130 people
Shelter C: 200 people
Shelter H: 40 people (DH + EH + FH + GH = 20 + 4 + 7 + 9 = 40 )
Shelter I: 20 people

Maximum Flow: 150 + 130 + 200 + 40 + 20 = 540 people
Hence, in this case, with the evacuation need of 300 people, the existing infrastructure is sufficient for evacuation.

Time Complexity:
The number of augmenting paths is bounded by O(V⋅*E)
Since BFS is called for each augmenting path, and BFS takes O(E) time per iteration
Hence the time complexity of the Edmonds-Karp algorithm in this case is
O(V * E^2), where V is the number of vertices and E is the number of edges.

"""