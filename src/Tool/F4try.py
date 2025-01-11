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



