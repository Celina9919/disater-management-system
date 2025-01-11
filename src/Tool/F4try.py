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



