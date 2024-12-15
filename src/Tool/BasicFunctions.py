import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class DisasterManagementTool:
    def __init__(self, graph_type="directed_unweighted"):
        """Initialize an empty city map."""
        self.city_map = None  # will be loaded later
        self.node_labels = []  # store names of nodes (A,B,C)
        self.graph_type = graph_type  # specify the graph type
        self.important_points = {}  # store important points and distance to intersections using DICTIONARY
        self.impassable_roads = []  # array list of impassable roads
        self.road_types = {}  # road types (land, waterway)

    def load_city_map(self, adjacency_matrix, node_labels=None):
        #define method
        #adjacency-matrix : sqaute grid for the matrix
        #node_labels A, B, C

        """Load a city map from an adjacency matrix."""
        self.city_map = np.array(adjacency_matrix)
        self.node_labels = node_labels if node_labels else [chr(65 + i) for i in range(len(adjacency_matrix))]
        #chr(65+i) creates character, 65 is A.. chr 65+1 is B
        #IF NO NODES GIVEN, THIS FUNCTION GIVES LABELS
        print(f"{self.graph_type.capitalize()} city map loaded successfully.")
        
    def display_city_map(self):
        """Display the city map as a graph using NetworkX and Matplotlib."""
        if self.city_map is None:
            print("No city map loaded.")
            return
        
        # Initialize appropriate NetworkX graph
        if self.graph_type in ["directed_unweighted", "directed_weighted"]:
            G = nx.DiGraph()  # Directed graph
        else:
            G = nx.Graph()  # Undirected graph
        
        # Add nodes
        for node in self.node_labels: #loop goes through each row (each node)
            G.add_node(node) #adds node to the graph , adding anew city location to the map

        # Add edges based on the adjacency matrix
        for i in range(len(self.city_map)): #loop goes through each row (each node)
            for j in range(len(self.city_map[i])):
                if self.city_map[i][j] != 0:  # Only add an edge if there is a non-zero value
                    # Check for weighted graph type
                    if self.graph_type in ["directed_weighted", "undirected_weighted"]:
                        G.add_edge(self.node_labels[i], self.node_labels[j], weight=self.city_map[i][j])
                    else:
                        G.add_edge(self.node_labels[i], self.node_labels[j])

        # Define graph layout
        pos = nx.spring_layout(G, k=2.5) #the looks for teh graph
        plt.figure(figsize=(8, 6), num=self.graph_type) #Combine figure size and title

        # Draw the graph
        edge_labels = nx.get_edge_attributes(G, 'weight') if "weighted" in self.graph_type else None
        nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
                         node_size=1500, font_size=12, arrows=True)
        if edge_labels:
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Display graph title
        plt.title(f"City Map of Schilda ({self.graph_type.replace('_', ' ').capitalize()})")
        plt.show()

    def print_adjacency_matrix(self):
        """Print the current adjacency matrix of the city map."""
        if self.city_map is None:
            print("No city map loaded.")
            return
        
        print(f"\nCurrent Adjacency Matrix for {self.graph_type.capitalize()}:")
        print("   ", " ".join(self.node_labels))
        for i, row in enumerate(self.city_map):
            print(f"{self.node_labels[i]}  ", " ".join(map(str, row)))

###########B2 FUNCTIONS STARTS HERE############
    def add_important_point(self, name, location, distance=None):  # name : hospital, location : node (e.g. A,B), distance : any value
        """Add important point at location, which may not be an existing intersection."""
        self.important_points[name] = (location, distance)  # call dictionary that initialised earlier
        # why use DICTIONARY : can store name as key, location & distance as a tuple
        print(f"Important point '{name}' added at location '{location}' with distance {distance} to nearest intersection.") 

    def mark_road_impassable(self, start, end):   #start & end points = nodes
        """Mark a road between start and end as impassable."""
        if (start, end) not in self.impassable_roads: #check alrd marked or not
            self.impassable_roads.append((start, end)) #add & store in self (initialised earlier)
            print(f"Road from {start} to {end} marked as impassable.")
            
    def add_road_type(self, start, end, road_type): # star & end = nodes , road_type = waterway/land
        """Specify whether a road between two points is a 'land route' or 'waterway'."""
        if road_type not in ['land', 'waterway']:
            print(f"Invalid road type. Must be 'land' or 'waterway'.")
            return
        self.road_types[(start, end)] = road_type #store in DICTIONARY (initialised earlier) 
        # key : start, end
        print(f"Road from {start} to {end} set as {road_type}.")
            
    