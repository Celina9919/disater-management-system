"""
BFS(Breadth-First Search) chosen

Why? :
- can easily handle multiple staging areas and deployment sites simultaneously
-BFS explores all nodes at the current level before moving to the next level, 
ensuring fair distribution of resources across deployment sites
- The level-by-level approach makes it easy to implement 
**priority-based** deployment when needed
- BFS naturally finds the shortest paths between 
staging areas and deployment sites

Why not djikstra? :
Overkill for this problem as we care more about:
-num of hops (BFS is optimal for this)
-avail capacity along paths
-fair distribution of resources

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

# Convert to directed graph for deployment planning
deployment_map = nx.DiGraph()

# Copy nodes and edges to directed graph
for u, v, data in G.edges(data=True):
    deployment_map.add_edge(u, v, capacity=data['weight'])
    deployment_map.add_edge(v, u, capacity=data['weight'])

# Assign attributes to nodes
node_attributes = {
    'A': "Hospital",
    'B': "Rescue Station",
    'C': "Government Building",
    'D': "Evacuation Point",
    'E': "Boat Rescue",
    'F': "Emergency Service",
    'G': "Supply Point",
    'H': "Staging Area", #main staging area
    'I': "Staging Area" #2nd staging area
}
nx.set_node_attributes(deployment_map, node_attributes, "description")

# how many units r required at KEY DEPLOYMENT SITES
deployment_needs = {
    'B': 30,  # rescue stat site needs 30 units
    'E': 20,  
    'F': 25   
}

#  how many units ea SA can provide
staging_areas = {
    'H': 50,  # main staging area
    'I': 30   # 2nd staging area
}

# Add capacities as node attributes
nx.set_node_attributes(deployment_map, staging_areas, "capacity")

# Define deployment routes and their capacities
routes = {
    ('H', 'B'): 25,  # main - rescue stat
    ('H', 'E'): 15,  # main - boat rescue
    ('H', 'F'): 20,  # main - emergency service
    ('I', 'B'): 20,  # 2nd - to rescue stat
    ('I', 'E'): 15,  # 2nd - boat rescue
    ('I', 'F'): 15   # 2nd - emergency service
}

# update capacities for deployment routes
for (start, end), capacity in routes.items():
    if deployment_map.has_edge(start, end):
        deployment_map[start][end]['capacity'] = capacity

# init deployment tracking
deployment_details = {(u, v): 0 for u, v in deployment_map.edges()}
#tracks num of units deployed 4 each edge

# calc total available capacity from staging areas
total_staging_capacity = sum(staging_areas.values())

if deployment_map.has_edge('F', 'E'):
    deployment_map['F']['E']['type'] = 'Impassable'
    deployment_map['E']['F']['type'] = 'Impassable'  

if deployment_map.has_edge('E', 'I'):
    deployment_map['E']['I']['type'] = 'Waterway'
    deployment_map['I']['E']['type'] = 'Waterway'

########BFS
def bfs_deployment(graph, start_node, target_node, required_units):
    """
    Performs BFS to find a path from a staging area (start_node) to a deployment site (target_node)
    """
    visited = set() #keep track have vsited or not, to avoid cycles
    queue = [(start_node, [start_node])] #stores node to explore next, along w current path
    #initial : start_node w empty path
    
    while queue: #while nodes to explore, the fx DEQUEUES node and look at al connected neighbours
        (vertex, path) = queue.pop(0) #dequeues
        for next_node in set(graph[vertex]) - visited: #for next node of current node, if not visited, add to queue
            # Skip edges marked as 'Impassable'
            if graph[vertex][next_node].get('type') == 'Impassable':
                continue
            if next_node == target_node: #return
                return path + [next_node]
            queue.append((next_node, path + [next_node]))
            visited.add(next_node)
    return None #no path

# deploy units from staging areas to deployment sites
def deploy_units():
    deployment_results = {} #stores the result of deployment: num of units deployed n path used
    
    
    for site, needed in deployment_needs.items(): #for ea depl node, CHECK how many units needed
        deployed = 0 #init counter 
        deployment_results[site] = {'total_deployed': 0, 'paths': []} #tracks units alrd deployed
        
        # deploying from each staging area
        for staging in staging_areas.keys():
            if deployed >= needed: #ea SA : checks if req number of units have been deployed
                break
            
            #calls fx bfs_deployment : to find a path from current SA to current deployment node   
            path = bfs_deployment(deployment_map, staging, site, needed - deployed) #needed-deployed : deploy remaining needs #checks
            
            if path:
                # calc available capacity along the path
                available_capacity = min(
                    min(deployment_map[u][v]['capacity'] - deployment_details.get((u, v), 0)
                        for u, v in zip(path[:-1], path[1:])),
                    staging_areas[staging], #avail units in SA
                    needed - deployed #remaining units needed at deploy node
                )
                
                if available_capacity > 0:
                    # update flow of units along ea edge in path
                    for u, v in zip(path[:-1], path[1:]):
                        deployment_details[(u, v)] = deployment_details.get((u, v), 0) + available_capacity
                    
                    
                    ####DEPLOYED UNITS (update)
                    deployed += available_capacity
                    deployment_results[site]['total_deployed'] += available_capacity
                    deployment_results[site]['paths'].append({
                        'path': path,
                        'units': available_capacity
                    })
                    
    
                    staging_areas[staging] -= available_capacity 
                    # update staging area capacity : reduced by num of units deployed alrd
    
    return deployment_results 

deployment_results = deploy_units() 

# Visualize 
def visualize_deployment(graph, deployment_results, title="Emergency Services Deployment Visualization"):
    pos = nx.spring_layout(graph, seed=42, k=10)
    plt.figure(figsize=(12, 8))
    
    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color="lightblue")
    
    edge_colors = []
    edge_widths = []
    edge_labels = {}
    
    for u, v, data in graph.edges(data=True):
        if data.get('type') == 'Impassable':  # Impassable edge
            edge_colors.append('black')
            edge_widths.append(3)
            edge_labels[(u, v)] = 'Impassable'
        elif data.get('type') == 'Waterway':  # Waterway edge
            edge_colors.append('blue')
            edge_widths.append(2)
            edge_labels[(u, v)] = 'Waterway'
        elif (u, v) in routes or (v, u) in routes:  # Regular deployment routes
            edge_colors.append('red')
            edge_widths.append(2)
        else:
            edge_colors.append('gray')
            edge_widths.append(1)
    
    nx.draw_networkx_edges(graph, pos, width=edge_widths, edge_color=edge_colors, alpha=0.7)
    
    node_labels = {}
    for node, data in graph.nodes(data=True):
        description = data.get('description', '')
        capacity = data.get('capacity', '')
        if capacity:
            node_labels[node] = f"{node}: {description}\n{capacity}"
        else:
            node_labels[node] = f"{node}: {description}"
    
    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=8)
    
    edge_labels = {}
    for u, v, data in graph.edges(data=True):
        if (u, v) in routes:
            flow = deployment_details.get((u, v), 0)
            capacity = data['capacity']
            edge_labels[(u, v)] = f"{flow}/{capacity}"
    
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title(title)
    plt.axis('off')
    plt.show()


print("\nDeployment Results:")
for site, result in deployment_results.items():
    print(f"\nSite {site} ({node_attributes[site]}):")
    print(f"Total units deployed: {result['total_deployed']}/{deployment_needs[site]}")
    print("Deployment paths:")
    for path_info in result['paths']:
        path_str = " -> ".join(path_info['path'])
        print(f"  {path_str}: {path_info['units']} units")


visualize_deployment(deployment_map, deployment_results)

"""
Time Complexity 

FX 1 (bfs_deployment): uses ea node, ea edge
Thus, O(V + E) or O(n + E)

FX 2 (deploy_units) : 
-uses iteration from deployment_needs, O(D), D = num of deployment sites 
-uses iteration of SA , O(SA), SA = num of staging areas
-combination : called bfs O(V + E) , path capacity O(P), P = path length,
updates deployment details : O(P)

TOTAL TIME COMPLEXITY : 
O(D * S * ((V + E) + V)) = O(D * S * (2V +E))
O(D * S * (2V +E)) = O(D * S * (V +E)) 
- 2 ignore, Big O notation drop constants, doesnt care

"""





