import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load adjacency matrix
file_path = 'src/Data/undirected_weighted_graph.txt'
adjacency_matrix = pd.read_csv(file_path, sep='\s+', index_col=0)  # Updated to use sep='\s+' instead of delim_whitespace

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

# Evacuation needs (source is 'D')
evacuation_needs = 300

# Add routes from the source (D) to the shelters
routes = {
    ('D', 'A'): 150,
    ('D', 'B'): 130,
    ('D', 'C'): 200,
    ('D', 'H'): 20,
    ('D', 'I'): 20
}
for (start, end), capacity in routes.items():
    city_map.add_edge(start, end, capacity=capacity)

# Add optional waterway routes
waterway_routes = {
    ('D', 'I'): 50
}
for (start, end), capacity in waterway_routes.items():
    city_map.add_edge(start, end, capacity=capacity)

# Calculate the maximum flow
flow_value, flow_dict = nx.maximum_flow(city_map, 'D', 'A', flow_func=nx.algorithms.flow.edmonds_karp)
for sink in ['B', 'C', 'H', 'I']:
    flow, flow_details = nx.maximum_flow(city_map, 'D', sink, flow_func=nx.algorithms.flow.edmonds_karp)
    flow_value += flow
    for key, value in flow_details.items():
        if key in flow_dict:
            flow_dict[key].update(value)
        else:
            flow_dict[key] = value

# Output results
print(f"Maximum Flow: {flow_value}")
print("Flow Details:")
for source, targets in flow_dict.items():
    for target, flow in targets.items():
        if flow > 0:
            print(f"  {source} -> {target}: {flow}")

# Save results to CSV
def save_flow_to_csv(graph, flow_dict, filename="evacuation_flow.csv"):
    data = []
    for source, targets in flow_dict.items():
        for target, flow in targets.items():
            if flow > 0:
                capacity = graph[source][target].get('capacity', 0)
                route_type = "Waterway" if (source, target) in waterway_routes else "Road"
                data.append([source, target, flow, capacity, route_type])
    df = pd.DataFrame(data, columns=['Source', 'Target', 'Flow', 'Capacity', 'Route Type'])
    df.to_csv(filename, index=False)
    print(f"Flow details saved to {filename}")

save_flow_to_csv(city_map, flow_dict)

# Visualization
def visualize_evacuation_flow(graph, flow_dict, title="Evacuation Flow Visualization"):
    pos = nx.spring_layout(graph, seed=42, k=3)
    plt.figure(figsize=(12, 8))

    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color="lightblue")
    
    edge_colors = []
    for u, v, data in graph.edges(data=True):
        flow = flow_dict[u][v] if u in flow_dict and v in flow_dict[u] else 0
        if (u, v) in waterway_routes:
            edge_colors.append("blue")
        else:
            edge_colors.append("gray")

    nx.draw_networkx_edges(graph, pos, width=2, alpha=0.7, edge_color=edge_colors)
    
    node_labels = {node: f"{node}: {data.get('description', 'No description')}" for node, data in graph.nodes(data=True)}
    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=10, font_color="black")

    edge_labels = {}
    for u, v, data in graph.edges(data=True):
        flow = flow_dict[u][v] if u in flow_dict and v in flow_dict[u] else 0
        capacity = data.get('capacity', 0)
        edge_labels[(u, v)] = f"Flow: {flow}/{capacity}"

    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="red", font_size=8)
    plt.title(title, fontsize=14)
    plt.axis("off")
    plt.show()

visualize_evacuation_flow(city_map, flow_dict)

# Decision
if flow_value >= evacuation_needs:
    print("The existing infrastructure is sufficient for evacuation.")
else:
    print("Additional infrastructure is needed for evacuation.")