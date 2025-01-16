"""
Edmond-Karp : an implementation of the Ford-Fulkerson method 
to calculate the maximum flow in a flow network
- repeatedly finding augmenting paths in the residual graph 
and pushing flow along them
    
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def edmonds_karp(graph, source, sink):
    """
    Implements Edmonds-Karp algorithm to find maximum flow in a network
    
    Args:
        graph (networkx.DiGraph): Directed graph with capacity attributes on edges
        source (str/int): Source node
        sink (str/int): Sink node
    
    Returns:
        flow_value (float): Maximum flow value
        flow_dict (dict): Dictionary of flows {(u,v): flow_value}
    """
    
    def bfs(residual_graph, source, sink):
        """Helper BFS function to find augmenting paths
        args : 
        -residual_graph: The graph that tracks the available 
        capacities (remaining capacities) of edges
        - source
        -sink
        """
        
        visited = {node: False for node in residual_graph.nodes()}
        #init a dict : tracks whether each node has been visited during the BFS 
        
        parent = {node: None for node in residual_graph.nodes()}
        #init a dict : stores the parent node of each node in the path, i
        # it helps reconstruct the augmenting path once the sink is reached
        
        queue = [source]
        #FIFO queue that stores the nodes to be explored
        #BFS algorithm processes nodes level-by-level, adding adjacent nodes to the queue as it visits them
        
        visited[source] = True
        #started BFS from source, mark as visited
        
        while queue: #core of BFS
            u = queue.pop(0) #dequeue 1st node from queue
            #u : current node being processed
            
            for v in residual_graph.neighbors(u):
                #returns the neighboring nodes v that are directly connected to u in residual graph 
                #nodes that we can potentially send flow to
                
                if not visited[v] and residual_graph[u][v]['capacity'] > 0: #check if v is not visited
                    #check if we can push flow through that edge (positive residual)
                    queue.append(v) #add node v to the queue to explore it in subsequent steps
                    visited[v] = True
                    parent[v] = u #records that we reached v from u, used to reconstruct the path once the sink is reached 
                    
                    if v == sink: #if reach this, we found augmenting path
                        #from source to sink
                        path = [] #init list : to store nodes in path
                        current = sink
                        #start from  sink node n trace back to the source using the parent dictionary
                        #for ea node current, insert it at the beginning of the path list (path.insert(0, current))
                        while current is not None:
                            path.insert(0, current)
                            current = parent[current]
                            #move to parent of current (current = parent[current]) 
                            #until we reach the source (where current will be None)
                            
                        return path
        return None #if no augmenting path



#########MAIN FUNCTION LOGIC : EDMOND KARP
    # init residual graph and flow
    residual_graph = graph.copy() #create a copy of the original graph to work with
    #residual graph tracks the remaining available capacity on each edge
    flow_dict = {(u,v): 0 for (u,v) in graph.edges()} 
    #dict : keeps track of the flow on each edge
    flow_value = 0
    #tracks the total flow in the network
    
    # find augmenting paths and update flows
    while True:
        path = bfs(residual_graph, source, sink)
        #call the BFS function: find an augmenting path from the source to the sink
        if not path:
            break
            
        # Find minimum capacity in the path
        path_flow = float('inf') #init store the minimum capacity along the path
        for i in range(len(path)-1): # for ea pair of consecutive nodes (u, v) in the path, 
            #check the capacity of the edge from u to v in the residual graph
            
            u, v = path[i], path[i+1]
            path_flow = min(path_flow, residual_graph[u][v]['capacity'])
            #update path_flow to be the minimum of the current path_flow and the residual capacity of the edge from u to v
            #ensures that the flow we push along the path does not exceed the capacity of any edge in the path
        
        # update residual capacities and flows
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            flow_dict[(u,v)] = flow_dict.get((u,v), 0) + path_flow
            #add flow path_flow to the existing flow on the edge (u, v)
            residual_graph[u][v]['capacity'] -= path_flow
            #reduuce residual capacity of the edge (u, v) by path_flow since we are pushing flow along that edge
            
            # Add reverse edge if it doesn't exist
            if not residual_graph.has_edge(v, u):
                residual_graph.add_edge(v, u, capacity=0) #if theres no already a reverse edge from v to u in the residual graph, 
                #add it with zero capacity
            residual_graph[v][u]['capacity'] += path_flow
            
        flow_value += path_flow #After processing the current augmenting path 
        #add the path_flow to the total flow (flow_value)
    
    return flow_value, flow_dict

def visualize_evacuation_flow(graph, flow_dict, title="Evacuation Flow Visualization"):
    """
    Visualizes the evacuation flow network
    """
    pos = nx.spring_layout(graph, seed=42, k=5)
    plt.figure(figsize=(12, 8))

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color="rosybrown")

    # Draw edges
    edge_colors = []
    shelter_nodes = ['A', 'B', 'C', 'H', 'I']
    for u, v in graph.edges():
        if u == 'D' and v in shelter_nodes:
            edge_colors.append('red')
        else:
            edge_colors.append('gray')

    nx.draw_networkx_edges(graph, pos, width=2, alpha=0.7, edge_color=edge_colors)

    # Add node labels
    node_labels = {}
    for node, data in graph.nodes(data=True):
        description = data.get('description', 'No description')
        capacity = data.get('capacity', None)
        if capacity:
            node_labels[node] = f"{node}: {description}\n{capacity}"
        else:
            node_labels[node] = f"{node}: {description}"

    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=10, font_color="black")

    # Add edge labels
    edge_labels = {}
    for (u, v) in graph.edges():
        flow = flow_dict.get((u, v), 0)
        capacity = graph[u][v]['capacity']
        edge_labels[(u, v)] = f"{flow:.0f}/{capacity}"

    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color="blue", font_size=8)
    plt.title(title, fontsize=14)
    plt.axis("off")
    plt.show()

# Load and setup graph
file_path = 'src/Data/undirected_weighted_graph.txt'
adjacency_matrix = pd.read_csv(file_path, sep=r'\s+', index_col=0)

# Create graph from adjacency matrix
G = nx.from_pandas_adjacency(adjacency_matrix, create_using=nx.Graph)
city_map = nx.DiGraph()
for u, v, data in G.edges(data=True):
    city_map.add_edge(u, v, capacity=data['weight'])
    city_map.add_edge(v, u, capacity=data['weight'])

# Node attributes
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

# Update evacuation route capacities
routes = {
    ('D', 'A'): 150,
    ('D', 'B'): 130,
    ('D', 'C'): 200,
    ('D', 'H'): 20,
    ('D', 'I'): 20
}

for (start, end), capacity in routes.items():
    if city_map.has_edge(start, end):
        city_map[start][end]['capacity'] = capacity

# Calculate flow for each shelter
shelter_nodes = ['A', 'B', 'C', 'H', 'I']
total_flow = 0
all_flows = {}

# Process each shelter
for shelter in shelter_nodes:
    # Create a copy of the graph for this shelter
    shelter_graph = city_map.copy()
    
    # Remove other shelters to ensure independent paths
    for other_shelter in shelter_nodes:
        if other_shelter != shelter:
            shelter_graph.remove_node(other_shelter)
    
    # Calculate maximum flow for this shelter
    flow_value, flow_dict = edmonds_karp(shelter_graph, 'D', shelter)
    
    # Update total flow and store flow details
    total_flow += flow_value
    for (u, v), flow in flow_dict.items():
        if flow > 0:
            all_flows[(u, v)] = all_flows.get((u, v), 0) + flow

    # Print flow details for this shelter
    print(f"\nShelter {shelter}:")
    for (u, v), flow in flow_dict.items():
        if flow > 0:
            print(f"  {u} -> {v}: {flow:.0f}")

print(f"\nTotal Maximum Flow: {total_flow:.0f}")

# Update the main graph with the calculated flows
for (u, v) in city_map.edges():
    city_map[u][v]['flow'] = all_flows.get((u, v), 0)

# Visualize the final flow
visualize_evacuation_flow(city_map, all_flows)

"""
TIME COMPLEXITY 

-BFS : O(|V| + |E|)

- MAIN COMPLEXITY : 
-Each time we find an augmenting path, we increase the flow by at least 1 unit
-For each augmenting path found, at least one edge becomes saturated
-Each edge can become saturated at most |V| times (proven by Edmonds and Karp)
Thus, the maximum number of augmenting paths : O(|V|⋅|E|)

Total Calc : 
-Main loop runs O(|V|⋅|E|) times
-each iteration performs a BFS taking O(|V| + |E|) time

Total complexity: 
O(|V|⋅|E|) * O(|V| + |E|) = O(|V|⋅|E|²)

    
"""