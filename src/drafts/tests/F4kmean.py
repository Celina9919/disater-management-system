"""
Using K-Means Clustering Algorithm to add 2 additional supply points
K-Means Clustering → Iterative partitioning of nodes.
Dijkstra's Algorithm → For distance calculations.


GOAL : to minimize the average distance from all relief forces to the nearest 
supply point and distribute relief forces evenly

why not k-means :
-K-Means doesn't work well with graphs because it can choose center points (centroids) that aren't 
on the graph
- could be located anywhere, even in places that don't exist or aren't connected by roads. 
- This makes calculating distances to those points tricky

"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

#use undirected
file_path = 'src/Data/undirected_weighted_graph.txt'
adjacency_matrix = pd.read_csv(file_path, delim_whitespace=True, index_col=0)

# create a graph from the adjacency matrix
G = nx.Graph()
for i, row in adjacency_matrix.iterrows():
    for j, weight in row.items():
        if weight > 0 and i != j:
            G.add_edge(i, j, weight=weight)

# node descriptions
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

############ K-Means Clustering Algorithm

######1
def initialize_centroids(nodes, k): # initialize random Centroids
    return random.sample(nodes, k) # fx randomly selects k(2, defined below) initial centroids

######2
# assign Nodes to Nearest Centroid
def assign_clusters(graph, centroids): ## assigns each node to the closest centroid using the shortest path
    clusters = {centroid: [] for centroid in centroids} #initializes a 'dictionary' clusters : will store the nodes assigned to each centroid
    for node in graph.nodes(): #for ea node, 
        if node not in centroids: 
            distances = [nx.shortest_path_length(graph, node, centroid, weight='weight') for centroid in centroids] 
            #calc shortest path to ea CENTROID (code above)
            closest_centroid = centroids[distances.index(min(distances))] #assign shortest path from node to ea CENTROID 
            #distances.index(min(distances) finds the centroid w smallest distance
            clusters[closest_centroid].append(node) #add to cluster dict
    return clusters


######3
#updates centroids : finding the node with the minimum average distance to others
def update_centroids(graph, clusters):
    new_centroids = [] #init empty list to store UPDATED centroids
    for nodes in clusters.values(): #for ea node,
        min_total_distance = float('inf') #init a variable : to keep track min total distance of a CLUSTER
        best_node = None #init a variable : store the node that will become the new centroid for THIS clister.
        for node in nodes: 
            total_distance = sum(nx.shortest_path_length(graph, node, other, weight='weight') for other in nodes)
            #calc total distance from the current node to all other nodes in the same cluster
            # idea : FIND NODE IN THAT CLUSTER that MINIMIZES the total distance to all other nodes
            if total_distance < min_total_distance:
                min_total_distance = total_distance
                #if the current total_distance is < min_total_distance(previously calc in fx bfr), update the minimum distance 
                best_node = node
        new_centroids.append(best_node) #once best node found, best node added to new_centroiids list
        
    return new_centroids



# run K-Means iteratively
def k_means(graph, k=2, max_iter=10): #iterating 10 times, back from 1-3
    nodes = list(graph.nodes()) #convert nodes to list
    centroids = initialize_centroids(nodes, k) #CALLING fx 1 : initialize centroids
    for _ in range(max_iter): #loop max_iter
        clusters = assign_clusters(graph, centroids) #CALLING fx 2: assign nodes to closest centorids
        new_centroids = update_centroids(graph, clusters) #CALLING fx 3:  update centroids based on the new clusters
        if new_centroids == centroids: #if same, no iterations, break
            break
        centroids = new_centroids #
    return clusters

# apply K-Means Clustering
clusters = k_means(G, k=2)

# Display the final centroids (selected supply points)
final_centroids = list(clusters.keys()) #EXTRACTS list of centroids(keys frm 'clusters' dict)
print(f"Selected Supply Points: {final_centroids}") #see on console, whoch final selections of centroids

# display distances from each supply point to its clustered nodes
for centroid, nodes in clusters.items():
    print(f"Distances from {centroid} to its clustered nodes:")
    for node in nodes:
        try:
            distance = nx.shortest_path_length(G, source=centroid, target=node, weight='weight')
            print(f"  {centroid} -> {node}: {distance}")
        except nx.NetworkXNoPath:
            print(f"  {centroid} -> {node}: No path found")


# Visualization
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(10, 10))

# gighlight centroids in yellow and other nodes in brown
node_colors = ["yellow" if node in final_centroids else "rosybrown" for node in G.nodes]
nx.draw_networkx_nodes(G, pos, node_size=800, node_color=node_colors)

# add node labels with descriptions
nx.draw_networkx_labels(G, pos, labels={node: f"{node}: {data.get('description', '')}" for node, data in G.nodes(data=True)}, font_size=8, font_color="navy")


edge_colors = []
for u, v, data in G.edges(data=True):
    if any(u == centroid and v in clusters[centroid] or v == centroid and u in clusters[centroid] for centroid in final_centroids):
        data['color'] = "green"  #GREEN AS CENTROIDS TO RELIEFS
    else:
        data['color'] = "lightgray"  


edge_colors = [data.get("color", "lightgray") for _, _, data in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1.5)


edge_labels = {(u, v): f"{int(d['weight'])}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=8)

plt.title("Graph with K-Means Clustering Supply Points Highlighted")
plt.show()




"""
Time Complexity 

FX 1 : uses random sample, k 
Thus, O(k) complexity

FX 2 : uses for ea nodes(n), centroids(k), also uses djikstra algo O(|E| + |V|log|V|))
Thus now : O(n * k * (|E| + |V|log|V|)),
|V| is number of vertices(nodes) and |E| is number of edges 

FX 3 : uses ea cluster (k clusters, k =2), ea node in cluster (n/k), 
ea other node in same cluster (n/k), + shortest path (djikstra)

Thus now total complexity :
O(k * (n/k) * (n/k) * (|E| + |V|log|V|)) = O(n² * (|E| + |V|log|V|)/k)

Iteration fx : called all 3 fx above

TOTAL TIME COMPLEXITY : 
O(max_iter * (
    n * k * (|E| + |V|log|V|) +                  
    n² * (|E| + |V|log|V|)/k                     
))

where V = nodes, E = edges 

"""