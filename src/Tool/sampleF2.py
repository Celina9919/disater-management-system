"""
Use Maximum Flow Algorithms (specifically, the Edmonds-Karp Algorithm,
Edmonds-Karp algorithm uses Breadth First Search (BFS) to find augmented paths to increase flow) to determine
whether the existing infrastructure can handle the evacuation demand
from assembly points to emergency shelters, considering road and water routes.

The Edmonds-Karp algorithm works by using Breadth-First Search (BFS)
to find a path with available capacity from the source to the sink (called an augmented path),
and then sends as much flow as possible through that path.

The Edmonds-Karp algorithm continues to find new paths to send more flow through until the maximum flow is reached.
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

file_path = 'src/Data/undirected_weighted_graph.txt'

adjacency_matrix = pd.read_csv(file_path, delim_whitespace=True, index_col=0)

G = nx.from_pandas_adjacency(adjacency_matrix, create_using=nx.Graph) #undirected

# Convert the undirected graph to a directed graph for Edmonds-Karp algorithm
city_map = nx.DiGraph()

# Copy all nodes and edges to the directed graph
for u, v, data in G.edges(data=True):
    city_map.add_edge(u, v, capacity=data['weight'])  # Adding capacity as weight
    city_map.add_edge(v, u, capacity=data['weight'])  # Reverse direction for undirected graph


# Input data
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


shelters = {
    'A': 200,  # Hospital shelter 200 people
    'B': 150,  # Rescue Station shelter 150 people
    'C': 250,  # Government Building shelter 250 people
    'H': 50,  # staging area shelter 50 people
    'I': 50,  # staging area shelter 50 people

}

evacuation_needs = {
    'D': 300  #300 ppl need to ecavuate
}


# add source
city_map.add_node('Source')
for point, people in evacuation_needs.items():
    city_map.add_edge('Source', point, capacity=people)

# add sink
city_map.add_node('Sink')
for shelter, capacity in shelters.items():
    city_map.add_edge(shelter, 'Sink', capacity=capacity)

routes = {
    ('D', 'A'): 150,  # Example: Route from A to X can handle 25 people
    ('D', 'B'): 130,  # Example: Route from A to Y can handle 15 people
    ('D', 'C'): 200,  # Example: Route from B to X can handle 10 people
    ('D', 'H'): 20,  # Example: Route from B to Y can handle 20 people
    ('D', 'I'): 20,  # Example: Route from B to Y can handle 20 people
}
for (start, end), capacity in routes.items():
    city_map.add_edge(start, end, capacity=capacity)

# add waterway (optional) (additional capacity)
waterway_routes = {
    ('D', 'I'): 50  
}
for (start, end), capacity in waterway_routes.items():
    city_map.add_edge(start, end, capacity=capacity)

# Calculate the maximum flow
flow_value, flow_dict = nx.maximum_flow(city_map, 'Source', 'Sink', flow_func=nx.algorithms.flow.edmonds_karp)
#nx.maximum_flow() = built in networkx func
# used to compute max flow btw source n sink

# Output results
print(f"Maximum Flow: {flow_value}")
print("Flow Details:")
for source, targets in flow_dict.items():
    for target, flow in targets.items():
        if flow > 0:
            print(f"  {source} -> {target}: {flow}")

    
###saving to csv  
def save_flow_to_csv(graph, flow_dict, filename="evacuation_flow.csv"):
    data = []
    for source, targets in flow_dict.items():
        for target, flow in targets.items():
            if flow > 0:  # Record only non-zero flows
                capacity = graph[source][target].get('capacity', 0)
                route_type = "Waterway" if (source, target) in waterway_routes else "Road"
                data.append([source, target, flow, capacity, route_type])
    df = pd.DataFrame(data, columns=['Source', 'Target', 'Flow', 'Capacity', 'Route Type'])
    df.to_csv(filename, index=False)
    print(f"Flow details saved to {filename}")
    
    save_flow_to_csv(city_map, flow_dict)
    
##### Visualization
def visualize_evacuation_flow(graph, flow_dict, title="Evacuation Flow Visualization"):
    pos = nx.spring_layout(graph, seed=42, k= 3)  
    plt.figure(figsize=(12, 8))

    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color="lightblue")
    nx.draw_networkx(graph, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=10)
    nx.draw_networkx_edges(graph, pos, width=2, alpha=0.7, edge_color="gray")
    
    edge_colors = []
    edge_labels = {}
    for u, v, data in graph.edges(data=True):
        flow = flow_dict[u][v] if u in flow_dict and v in flow_dict[u] else 0
        label = f"{flow}/{data.get('capacity', 0)}"
        edge_labels[(u, v)] = label
        edge_colors.append("blue" if (u, v) in waterway_routes else "gray")

    nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=2)
    nx.draw_networkx_labels(graph, pos, font_size=10, font_color="black")
    edge_labels = nx.get_edge_attributes(graph, 'capacity')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels= edge_labels, font_size=8, font_color="red")


    plt.title(title, fontsize=14)
    plt.axis("off")
    plt.show()

visualize_evacuation_flow(city_map, flow_dict)
    
# Decision based on the flow
total_demand = sum(evacuation_needs.values())
if flow_value >= total_demand:
    print("The existing infrastructure is sufficient for evacuation.")
else:
    print("Additional infrastructure is needed for evacuation.")
    

print(f"Maximum Flow: {flow_value}")
    
    
    
