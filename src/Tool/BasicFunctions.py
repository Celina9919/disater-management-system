import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class DisasterManagementTool:
    def __init__(self, graph_type="directed_unweighted"):
        """Initialize an empty city map."""
        self.city_map = None  # Will be loaded later
        self.node_labels = []  # Store names of nodes (A,B,C)
        self.graph_type = graph_type  # Specify the graph type
        self.important_points = {}  # Store important points and distance to intersections using DICTIONARY
        self.impassable_roads = []  # Array list of impassable roads
        self.road_types = {}  # Dictionary to store road types (land, waterway)

    def load_city_map(self, adjacency_matrix, node_labels=None):
        """Load a city map from an adjacency matrix."""
        self.city_map = np.array(adjacency_matrix) # Convert adjacency matrix to a NumPy array
        self.node_labels = node_labels if node_labels else [chr(65 + i) for i in range(len(adjacency_matrix))]
        print(f"{self.graph_type.capitalize()} city map loaded successfully.")
    
    # Initialize graph based on the graph type
        if self.graph_type in ["directed_unweighted", "directed_weighted"]:
            G = nx.DiGraph()  # Directed graph
        else:
            G = nx.Graph()  # Undirected graph

    # Add nodes to the graph
        for node in self.node_labels:
            G.add_node(node)

    # Add edges based on the adjacency matrix
        for i in range(len(self.city_map)):  # Loop through each node
            for j in range(len(self.city_map[i])):  # Loop through each neighbor
                if self.city_map[i][j] != 0:  # Only add an edge if there is a non-zero value
                # Check for weighted graph type, for weighted graph types, add weight to the edge
                    if self.graph_type in ["directed_weighted", "undirected_weighted"]:
                        G.add_edge(self.node_labels[i], self.node_labels[j], weight=self.city_map[i][j])
                    else:
                        G.add_edge(self.node_labels[i], self.node_labels[j])

        # Draw the graph
        edge_labels = nx.get_edge_attributes(G, 'weight') if "weighted" in self.graph_type else None # Get edge weights if present
        pos = nx.spring_layout(G, k=2.5)  # Layout for visualization
        nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', # General graph layout
                        node_size=1500, font_size=12, arrows=True)
        if edge_labels: # Display edge labels (weights) if present
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)


    def print_adjacency_matrix(self):
        """Print the current adjacency matrix of the city map."""
        if self.city_map is None:
            print("No city map loaded.")
            return
        
        print(f"\nCurrent Adjacency Matrix for {self.graph_type.capitalize()}:")
        print("   ", " ".join(self.node_labels))  # Print column headers (node labels)
        for i, row in enumerate(self.city_map):   # Print rows of the adjacency matrix
            print(f"{self.node_labels[i]}  ", " ".join(map(str, row)))

###########B2 FUNCTIONS STARTS HERE############ 
    def add_important_point(self, name, location, distance=None):  
        """Add important point at location, which may not be an existing intersection."""
        self.important_points[name] = (location, distance)  # Call dictionary that initialised earlier, that stores name, location, and distance in dictionary
        # why use DICTIONARY : can store name as key, location & distance as a tuple
        print(f"Important point '{name}' added at location '{location}' with distance {distance} to nearest intersection.") 

    def mark_road_impassable(self, start, end):   #start & end points = nodes
        """Mark a road between start and end as impassable."""
        if (start, end) not in self.impassable_roads: # Check if road is already marked as impassable or not 
            self.impassable_roads.append((start, end)) #add & store in self (initialised earlier)/ Add to the list of impassable roads
            print(f"Road from {start} to {end} marked as impassable.")
            
    def add_road_type(self, start, end, road_type): #start & end = nodes , road_type = waterway/land
        """Specify whether a road between two points is a 'land route' or 'waterway'."""
        if road_type not in ['land', 'waterway']:
            print(f"Invalid road type. Must be 'land' or 'waterway'.")
            return
        self.road_types[(start, end)] = road_type # Store road type in DICTIONARY (initialised earlier) 
        # key : start, end
        print(f"Road from {start} to {end} set as {road_type}.")
        
########GRAPH DISPLAYING##########
            
    def display_city_map(self):
        """display the city map as a graph with additional features that are just added"""
        if self.city_map is None:
            print("No city map loaded.")
            return
        
    # Initialize graph
        if self.graph_type in ["directed_unweighted", "directed_weighted"]:
            G = nx.DiGraph()  # Directed graph
        else:
            G = nx.Graph()  # Undirected graph
            
    # Add nodes to the graph 
        for node in self.node_labels: #loop goes through each row (each node)
            G.add_node(node) #adds node to the graph , adding a new city location to the map
            
        for i in range(len(self.city_map)):
                for j in range(len(self.city_map[i])):
                    if self.city_map[i][j] != 0 and (self.node_labels[i], self.node_labels[j]) not in self.impassable_roads:
                        G.add_edge(self.node_labels[i], self.node_labels[j])
                        
        # Graph layout
        pos = nx.spring_layout(G, k=2.5) # Layout for visualization (the looks for the graph)
        plt.figure(figsize=(8, 6), num=self.graph_type) # Combine figure size and title
        
        edge_colors = []  # Set roads/edges colors to differentiate to differentiate
        for u, v in G.edges():
            if (u, v) in self.impassable_roads:
                edge_colors.append('red')  # Impassable roads: red
            elif self.road_types.get((u, v)) == 'waterway':
                edge_colors.append('blue')  # Waterways : blue
            else:
                edge_colors.append('gray')  # Normal roads: gray
        
        # Draw the graph
        nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', edge_color=edge_colors,
                         node_size=1500, font_size=12, arrows=True)
        
        # Display important points on the map
        for point, (location, distance) in self.important_points.items():
            plt.text(pos[location][0], pos[location][1] + 0.1, f'{point} ({distance}m)' if distance else point,
                     fontsize=10, fontweight='bold', color='darkred')
        
        # Set the title and display the graph    
        plt.title(f"City Map of Schilda ({self.graph_type.replace('_', ' ').capitalize()})")
        plt.show()
        
    