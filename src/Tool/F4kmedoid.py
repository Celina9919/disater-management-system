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

######1
def custom_dijkstra(graph, start): #djikstra to find shortest paths from starting node to all other nodes in the graph
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
                weight = graph.edges[current_node, neighbor]['weight']
                #retrieves weight/distance btw current_node n its neighbour 
                
                distance = current_distance + weight
                #calc POTENTIAL new shortest dist to neighbour
                #by adding weight of edge
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    #if newly calc distance smaller, update
                    
                    heapq.heappush(pq, (distance, neighbor)) #push neighbour and its new dist to prio queue
    return distances

######2
def initialize_medoids(nodes, k): # initialize random Medoids
    return random.sample(nodes, k) # fx randomly selects k(2, defined below) initial medoids

######3
def assign_clusters(graph, medoids): ## assigns each node to the closest medoid using custom Dijkstra
    clusters = {medoid: [] for medoid in medoids} #initializes a 'dictionary' clusters : will store the nodes assigned to each medoid
    medoid_distances = {medoid: custom_dijkstra(graph, medoid) for medoid in medoids} #dict : where keys r medoids, and values are results of running
    
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
def update_medoids(graph, clusters): # updates medoids by finding node with minimum total distance in each cluster
    new_medoids = [] #init empty list to store UPDATED medoids
    for medoid, nodes in clusters.items(): #for ea cluster
        
        cluster_nodes = [medoid] + nodes
        #adds medoid itself to list of cluster nodes
        
        min_total_distance = float('inf')
        #init variable : store minimum total distance for each cluster
        
        best_node = None
        #init variable : store the best medoid
        
        for node in cluster_nodes:
            distances = custom_dijkstra(graph, node)
            #calc shortest paths from current node to all other nodes
            
            total_distance = sum(distances[other] for other in cluster_nodes if other != node)
            #calc total distance from this node to all other nodes in the cluster
            
            if total_distance < min_total_distance:
                min_total_distance = total_distance
                
                #if the current total_distance is < min_total_distance(previously calc in fx bfr), 
                # update the minimum distance 
                
                best_node = node
                
        new_medoids.append(best_node)
    return new_medoids

def calculate_total_cost(graph, clusters, medoids): #fx calc sum of shortest distances of a clustering solution 
    total_cost = 0 #store total dist 
    for medoid, cluster_nodes in clusters.items():
        distances = custom_dijkstra(graph, medoid) #call fx1 : retrieve shortest dist from current medoid to other nodes
        total_cost += sum(distances[node] for node in cluster_nodes)
        #sum distances from medoid to its cluster nodes and adds to total_cost
    return total_cost

# run K-Medoids iteratively
def k_medoids(graph, k=2, max_iter=10): #iterating 10 times, back from 1-4
    nodes = list(graph.nodes())
    current_medoids = initialize_medoids(nodes, k) #CALLING fx 2: initialize medoids
    current_clusters = None
    current_cost = float('inf')
    
    for _ in range(max_iter):
        new_clusters = assign_clusters(graph, current_medoids) #CALLING fx 3: assign nodes to closest medoids
        new_medoids = update_medoids(graph, new_clusters) #CALLING fx 4: update medoids based on new clusters
        new_cost = calculate_total_cost(graph, new_clusters, new_medoids)
        
        if new_cost >= current_cost: #if cost not improving, stop
            break
            
        current_medoids = new_medoids
        current_clusters = new_clusters
        current_cost = new_cost
        
    return current_clusters

# apply K-Medoids Clustering
clusters = k_medoids(G, k=2)

# Display the final medoids (selected supply points)
final_medoids = list(clusters.keys())
print(f"Selected Supply Points: {final_medoids}")

# display distances from each supply point to its clustered nodes
for medoid, nodes in clusters.items():
    print(f"Distances from {medoid} to its clustered nodes:")
    for node in nodes:
        distances = custom_dijkstra(G, medoid)
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
    if any(u == medoid and v in clusters[medoid] or 
           v == medoid and u in clusters[medoid] for medoid in final_medoids):
        data['color'] = "green"  #GREEN AS MEDOIDS TO RELIEFS
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

FX 2 : uses random sample, k 
Thus, O(k) complexity

FX 3 : calculates dijkstra for each medoid (k * E log V) and then 
assigns each node (n) to closest medoid by checking all medoids (k)
Thus, O(k * E log V + n * k)

FX 4 : for each cluster (k), calculate dijkstra for each node in cluster (n/k * E log V)
and sum distances to all other nodes in cluster (n/k)
Thus, O(k * (n/k * E log V * n/k)) = O(n² * E log V / k)

TOTAL TIME COMPLEXITY for one iteration: 
O(k + k * E log V + n * k + n² * E log V / k)

For max_iter iterations:
O(max_iter * (k + k * E log V + n * k + n² * E log V / k))

where:
V = vertices (nodes)
E = edges
n = total nodes
k = number of clusters
"""