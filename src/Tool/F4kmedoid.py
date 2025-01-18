"""
K-Medoids is a clustering algorithm similar to K-Means but uses actual data points (medoids) as 
cluster centers instead of the mean. 
- The algorithm works by initializing k medoids, assigning each data point to the nearest medoid, 
and then iteratively updating the medoids by minimizing the total distance within each cluster.

why: 
- good at finding the best places to put resources (like supply points) on a map, 
especially when some paths might be blocked or have extra difficulty, like waterways
- works by starting with random spots, checking which ones work best, 
and improving the spots until find the best ones.
-works directly with the nodes on the graph : ensuring that the center points (medoids) 
are real, existing locations on our map. 

total_cost : represents the sum of the shortest path distances 
from all nodes in the graph to their assigned medoid (supply point)

"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict
import heapq

file_path = 'src/Data/undirected_weighted_graph.txt'
adjacency_matrix = pd.read_csv(file_path, delim_whitespace=True, index_col=0)

G = nx.Graph()
for i, row in adjacency_matrix.iterrows():
    for j, weight in row.items():
        if weight > 0 and i != j:
            G.add_edge(i, j, weight=weight)

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
nx.set_node_attributes(G, node_attributes, 'description')

############ K-Medoids Algorithm

######1 DJIKSTRA + CONSIDERING WATERWAYS, IMPASSABLES
def custom_dijkstra(graph, start, impassables, waterways): #djikstra to find shortest paths from starting node to all other nodes in the graph
    distances = {node: float('inf') for node in graph.nodes()}
    #dict : store the shortest distance to each node
    
    distances[start] = 0
    pq = [(0, start)]
    #priority queue (min-heap) to manage nodes based 
    #on their current shortest distance
    
    visited = set()

    while pq: #runs as long there r nodes in the queue
        current_distance, current_node = heapq.heappop(pq)
        #pops node w the smallest distance from queue
        
        if current_node in visited:
            continue #if visited : skip 
        visited.add(current_node)
        
        for neighbor in graph.neighbors(current_node): #iterates all neighbouring node
            if neighbor not in visited:
                weight = graph.edges[current_node, neighbor].get('weight', 1)
                #retrieves weight/distance btw current_node n its neighbour 
                
                # penalize impassable obstacles (add weight = infinity on impassables, so that its path wont be shortest)
                if (current_node, neighbor) in impassables or (neighbor, current_node) in impassables:
                    weight = float('inf')  # impassable 
                
                # penalize waterways with additional weight (add weight  = +10, so that it wont be shortest)
                if (current_node, neighbor) in waterways or (neighbor, current_node) in waterways:
                    weight += 10  # waterway 
                
                distance = current_distance + weight
                #calc POTENTIAL new shortest dist to neighbour
                #by adding weight of edge
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    #if newly calc distance smaller, update
                    
                    heapq.heappush(pq, (distance, neighbor)) #push neighbour and its new dist to prio queue
    return distances

######2
def initialize_medoids(nodes, k, existing_supply_point='G'): # initialize random Medoids
    # ensure: existing supply point (node G) is always selected as one medoid
    
    best_medoids = None
    best_cost = float('inf')    
    
    available_nodes = [node for node in nodes if node != existing_supply_point]   
    #list :  nodes excluding fixed supply point (G)
    
    # try: every possible combination of 2 additional points (excl G) 
    #considering : G fixed, k= 3
    for i in range(len(available_nodes)):
        for j in range(i + 1, len(available_nodes)):
            
            # create : a pair of medoids (as candidates)
            # combining G w 2 selected nodes
            current_medoids = [existing_supply_point, available_nodes[i], available_nodes[j]]
            
            # calc clusters for this combination
            current_clusters = assign_clusters(G, current_medoids, obstacles, waterways)
            
            # calc total cost for this combination 
            # calls fx 4
            current_cost = calculate_total_cost(G, current_clusters, current_medoids, obstacles, waterways)
            
            # update best if : combination has lower cost
            if current_cost < best_cost:
                best_cost = current_cost
                best_medoids = current_medoids
    
    print(f"Best initial medoids found with cost: {best_cost}")
    return best_medoids

######3
def assign_clusters(graph, medoids, impassables, waterways): ## assigns each node to the closest medoid using custom Dijkstra
    clusters = {medoid: [] for medoid in medoids} #initializes a 'dictionary' clusters : will store the nodes assigned to each medoid
    medoid_distances = {medoid: custom_dijkstra(graph, medoid,impassables, waterways) for medoid in medoids} #dict : where keys r medoids, and values are results of running
    
    for node in graph.nodes(): #for ea node
        if node not in medoids: #skip nodes that r medoids
            
            distances = [medoid_distances[medoid][node] for medoid in medoids]
            #for each non-medoid, computes dist to every medoid using previously calculated shortest path results for all medoids
            
            closest_medoid = medoids[distances.index(min(distances))]
            #finds medoid that is closest to the current node
            
            clusters[closest_medoid].append(node)
            #adds node to cluster of closest medoid
    return clusters

######4
def calculate_total_cost(graph, clusters, medoids, impassables, waterways): #fx calc sum of shortest distances of a clustering solution 
    total_cost = 0 #store total dist 
    for medoid, cluster_nodes in clusters.items(): #iterates over each medoid n its assigned cluster
        
        distances = custom_dijkstra(graph, medoid, impassables, waterways) 
        #call fx1 : retrieve shortest dist from current medoid to other nodes
        
        total_cost += sum(distances[node] for node in cluster_nodes)
        #sum distances from medoid to its cluster nodes and adds to total_cost
        
    return total_cost

####5 : run K-Medoids iteratively
def k_medoids(graph, max_iter=10, obstacles=[], waterways=[], existing_supply_point="G"): #iterating 10 times, back from 1-4
    nodes = list(graph.nodes())
    #retrieves all graph nodes
    
    current_medoids = initialize_medoids(nodes, k=3, existing_supply_point=existing_supply_point)
    #init medoids: call fx 2
    
    #to store clusters, cost
    current_clusters = None
    current_cost = float('inf')
    
    print(f"Selected fixed medoids: {current_medoids}")
    
    # since we found best combination, we only need to run once to get final clusters
    # assign clusters 
    # calc their total cost for the initialized medoids
    new_clusters = assign_clusters(graph, current_medoids, obstacles, waterways)
    new_cost = calculate_total_cost(graph, new_clusters, current_medoids, obstacles, waterways)
    
    print(f"Final total cost: {new_cost}")
    return new_clusters

obstacles = [("F", "E")]  # F-E is impassable
waterways = [("E", "I")]  # E-I is a waterway

# apply K-Medoids Clustering
clusters = k_medoids(G, obstacles=obstacles, waterways=waterways)

# display the final medoids (selected supply points)
final_medoids = list(clusters.keys())
print(f"Selected Supply Points: {final_medoids}")

# display distances from each supply point to its clustered nodes
for medoid, nodes in clusters.items():
    print(f"Distances from {medoid} to its clustered nodes:")
    for node in nodes:
        distances = custom_dijkstra(G, medoid, obstacles, waterways)
        print(f"  {medoid} -> {node}: {distances[node]}")

# Visualization
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(10, 10))

node_colors = ["yellow" if node in final_medoids else "rosybrown" for node in G.nodes]
nx.draw_networkx_nodes(G, pos, node_size=800, node_color=node_colors)


nx.draw_networkx_labels(G, pos, labels={node: f"{node}: {data.get('description', '')}" 
                                       for node, data in G.nodes(data=True)}, 
                       font_size=8, font_color="navy")

edge_colors = []
for u, v, data in G.edges(data=True):
    if (u, v) in waterways or (v, u) in waterways:
        data['color'] = "blue"  # waterways
    elif (u, v) in obstacles or (v, u) in obstacles:
        data['color'] = "red"  #  impassable 
    elif any(u == medoid and v in clusters[medoid] or 
             v == medoid and u in clusters[medoid] for medoid in final_medoids):
        data['color'] = "green"  # GREEN FOR MEDOIDS
    else:
        data['color'] = "lightgray"  
         

edge_colors = [data.get("color", "lightgray") for _, _, data in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1.5)

edge_labels = {(u, v): f"{int(d['weight'])}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=8)

plt.title("Graph with K-Medoids Clustering Supply Points Highlighted")
plt.show()

"""
Time Complexity 

FX 1 (custom_dijkstra) : O(E log V) where E is edges and V is vertices

FX 2 :  nested loops to try all possible combinations of 2 additional points
- for n nodes, O(n²) combinations
- combination : assign_clusters: O(kV + kE log V), calculate_total_cost: O(kE log V)
- Total complexity: O(n² * (kV + kE log V)), where k =3
- Final : O(n² * (V + E log V))

FX 3 : calculates dijkstra for each medoid (k * E log V) and then 
- for ea node, find closest medoid: O(kV)
- Final: O(kE log V + kV), where k =3

FX 4 : - call custom_dijkstra(fx1) for each medoid: O(kE log V)
- for ea clushter : sums distances: O(V)
- Final : O(kE log V + V)

FX 5 : - initialize_medoids once: O(n² * (V + E log V))
- make on final assignment of clusters: O(kE log V + kV)

TOTAL TIME COMPLEXITY for one iteration: 
- max_iter : 10, k =3 --> dont affcet big O
- Final : O(n² * (V + E log V))

DOMINANT FACTOR :  
- initialize_medoids FX1: tries all possible combinations of additional supply points
- fixed node G + additional points :  O(n²) combinations
- for ea combination: calc distances and costs using Dijkstra's algorithm

where:
V = vertices (nodes)
E = edges
n = total nodes
k = number of clusters
"""