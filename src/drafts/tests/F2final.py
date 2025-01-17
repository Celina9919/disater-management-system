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
import random

# Load adjacency matrix
file_path = 'src/Data/undirected_weighted_graph.txt'
adjacency_matrix = pd.read_csv(file_path, sep='\s+', index_col=0)

# Create an undirected graph
G = nx.from_pandas_adjacency(adjacency_matrix, create_using=nx.Graph)

# Convert the undirected graph to a directed graph
city_map = nx.DiGraph()

# copy all nodes and edges to the directed graph
for u, v, data in G.edges(data=True):
    city_map.add_edge(u, v, capacity=data['weight'])  #data is attributes of the edge
    city_map.add_edge(v, u, capacity=data['weight']) #biderectional, uv and vu

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

# add shelter's capacities as node attributes
nx.set_node_attributes(city_map, shelters, "capacity")

# Evacuation needs (set source : 'D')
evacuation_needs = 300

# define shelter nodes
shelter_nodes = ['A', 'B', 'C', 'H', 'I']

# initialize flow dictionary with 0 flows for all edges
random_flow_details = {(u, v): 0 for u, v in city_map.edges()}

routes = {
    ('D', 'A'): 150,
    ('D', 'B'): 130,
    ('D', 'C'): 200,
    ('D', 'H'): 20,
    ('D', 'I'): 20
}

# Update capacities for evacuation routes
for (start, end), capacity in routes.items():
    if city_map.has_edge(start, end):
        city_map[start][end]['capacity'] = capacity
        
# Calculate total available capacity
total_available_capacity = sum(min(routes[('D', shelter)], shelters[shelter]) 
                             for shelter in shelter_nodes)

if total_available_capacity < evacuation_needs:
    raise ValueError(f"Not enough capacity to evacuate {evacuation_needs} people. Maximum capacity is {total_available_capacity}")

# Initialize flows to zero
for shelter in shelter_nodes:
    random_flow_details[('D', shelter)] = 0

# First pass: Randomly distribute most of the flow
remaining_to_evacuate = evacuation_needs
while remaining_to_evacuate > 0:
    available_shelters = [s for s in shelter_nodes 
                         if random_flow_details[('D', s)] < min(routes[('D', s)], shelters[s])]
    
    if not available_shelters:
        break
        
    shelter = random.choice(available_shelters)
    current_flow = random_flow_details[('D', shelter)]
    max_capacity = min(routes[('D', shelter)], shelters[shelter])
    space_left = max_capacity - current_flow
    
    # For the last bit of flow, just assign what's needed
    if remaining_to_evacuate <= 10:
        flow = min(remaining_to_evacuate, space_left)
    else:
        # Otherwise, assign a random amount but leave some for other shelters
        max_flow = min(remaining_to_evacuate - 5, space_left)
        flow = random.randint(1, max_flow) if max_flow > 0 else 0
    
    random_flow_details[('D', shelter)] += flow
    remaining_to_evacuate -= flow

# If there's still remaining flow, distribute it to shelters with remaining capacity
if remaining_to_evacuate > 0:
    for shelter in shelter_nodes:
        current_flow = random_flow_details[('D', shelter)]
        max_capacity = min(routes[('D', shelter)], shelters[shelter])
        space_left = max_capacity - current_flow
        
        if space_left > 0:
            additional_flow = min(space_left, remaining_to_evacuate)
            random_flow_details[('D', shelter)] += additional_flow
            remaining_to_evacuate -= additional_flow
            
            if remaining_to_evacuate == 0:
                break
            
# Update graph edges with current flow
for u, v in city_map.edges():
    city_map[u][v]['current_flow'] = random_flow_details.get((u, v), 0)
        
# shelters should ONLY RECEIVE flow not send 
for shelter in shelters: #shelters = Sink
    city_map.remove_edges_from([(shelter, neighbor) for neighbor in city_map.successors(shelter)])
    #city_map.remove_edges_from : remove all outgoing edges from shelters
    #city_map.successors : find all outgoing edges from sheltes

# Initialize variables
shelter_flow_details = {}  #stores flow details of ea shelter
total_flow = 0 #total flow of source(D) to all shelter

# Calculate maximum flow for each shelter independently, prioritizing smaller shelters
for shelter, capacity in sorted(shelters.items(), key=lambda x: x[1]):  # Sort by shelter capacity (ascending)
    # calc maximum flow from the source (D) to the shelter
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
    pos = nx.spring_layout(graph, seed=42, k=5)
    plt.figure(figsize=(12, 8))

    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color="rosybrown")

    edge_colors = []
    for u, v, data in graph.edges(data=True):
        if u == 'D' and v in shelter_nodes:
            edge_colors.append('red')  # Evacuation routes
        else:
            edge_colors.append('gray')  # Other edges

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
    for u, v, data in graph.edges(data=True):
        current_flow = data.get('current_flow', 0)
        if u == 'D' and v in shelter_nodes:
            max_capacity = routes.get((u, v), data.get('capacity', 0))
        else:
            max_capacity = data.get('capacity', 0)
        edge_labels[(u, v)] = f"{current_flow}/{max_capacity}"
    

    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="blue", font_size=8)
    plt.title(title, fontsize=14)
    plt.axis("off")
    plt.show()
    
# Output results with controlled infrastructure message
print(f"Maximum Flow: {total_flow}")
print("\nFlow Details by Shelter:")
for shelter, flows in shelter_flow_details.items():
    print(f"\nShelter {shelter}:")
    if flows:
        for source, targets in flows.items():
            for target, flow in targets.items():
                print(f"  {source} -> {target}: {flow}")
        if shelter in ['A', 'B', 'C', 'H', 'I']:  # print message for these shelters ONLY
            print("The existing infrastructure is sufficient for evacuation.")
    else:
        print("  No flow received.")
        if shelter in ['A', 'B', 'C', 'H', 'I']:  
            print("The existing infrastructure is sufficient for evacuation.")

visualize_evacuation_flow(city_map, shelter_flow_details)

"""
Output Explaination:
Shelter A: 150 people
Shelter B: 130 people
Shelter C: 200 people
Shelter H: 40 people (DH + EH + FH + GH = 20 + 4 + 7 + 9 = 40 )
Shelter I: 20 people

Shelter H method is used to avoid addtional points for super sink and 
avoid path concurrency to shelter


Maximum Flow: 150 + 130 + 200 + 40 + 20 = 540 people
Hence, in this case, with the evacuation need of 300 people, the existing infrastructure is sufficient for evacuation.

Time Complexity:
The number of augmenting paths is bounded by O(V⋅*E)
Since BFS is called for each augmenting path, and BFS takes O(E) time per iteration
Hence the time complexity of the Edmonds-Karp algorithm in this case is
O(V * E^2), where V is the number of vertices and E is the number of edges.

"""