import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class DisasterManagementTool:
    def __init__(self, graph_type="directed_unweighted"):
        """Initialize an empty city map."""
        self.city_map = None  #  # will be loaded later (adjacency matrix of the city)
        self.node_labels = [] # Store names of nodes (A, B, C, ...)
        self.graph_type = graph_type  # Specify the graph type (directed or undirected)

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
        """Display the city map as a graph using NetworkX and Matplotlib.
        Visualizes the adjacency matrix as a graph with nodes and edges."""
        
        # check if city map is loaded
        if self.city_map is None:
            print("No city map loaded.")
            return
        
        # init the appropriate NetworkX graph (directed or undirected)
        if self.graph_type in ["directed_unweighted", "directed_weighted"]:
            G = nx.DiGraph()  # Directed graph
        else:
            G = nx.Graph()  # Undirected graph
        
        # add nodes (nodes labeled as A, B, C, ...)
        for node in self.node_labels: # Loop goes through each row (each node)
            G.add_node(node) # Adds node to the graph, adding a new city location to the map

        # add edges based on the adjacency matrix
        for i in range(len(self.city_map)): #loop goes through each row (each node)
            for j in range(len(self.city_map[i])):
                if self.city_map[i][j] != 0:  # Only add an edge if there is a non-zero value
                    # Check for weighted graph type, if the graph is weighted, include the edge weight
                    if self.graph_type in ["directed_weighted", "undirected_weighted"]:
                        G.add_edge(self.node_labels[i], self.node_labels[j], weight=self.city_map[i][j])
                    else:
                        G.add_edge(self.node_labels[i], self.node_labels[j])

        # define graph layout (positioning of nodes in the visualization)
        pos = nx.spring_layout(G, k=2.5) # the looks for the graph
        
        # create figure for displaying the graph
        plt.figure(figsize=(8, 6), num=self.graph_type) # Set figure size and graph title
    

        # draw graph w optional edge labels if weighted
        edge_labels = nx.get_edge_attributes(G, 'weight') if "weighted" in self.graph_type else None
        nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
                         node_size=1500, font_size=12, arrows=True)
        if edge_labels:
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  # Draw edge labels for weighted edges

        # display graph title indicating the map and graph type
        plt.title(f"City Map of Schilda ({self.graph_type.replace('_', ' ').capitalize()})")
        plt.show()

    def print_adjacency_matrix(self):
        """Print the current adjacency matrix of the city map. 
        Displays the matrix with node labels and edge weights"""
        if self.city_map is None: # Check if city map is loaded
            print("No city map loaded.")
            return
        
        # print the adjacency matrix with node labels
        print(f"\nCurrent Adjacency Matrix for {self.graph_type.capitalize()}:")
        print("   ", " ".join(self.node_labels)) # Print node labels as column headers
        for i, row in enumerate(self.city_map):
            print(f"{self.node_labels[i]}  ", " ".join(map(str, row))) # Print each row with node label
            
if __name__ == "__main__":
    # create instance for unweighted directed graph
    tool_unweighted = DisasterManagementTool(graph_type="directed_unweighted")
    
    directed_unweighted_matrix = [
        #A, B, C, D, E, F, G, H, I, J
        [0, 1, 0, 0, 1, 0, 1, 1, 0, 1], # A
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0], # B
        [1, 0, 0, 1, 0, 0, 1, 1, 0, 0], # C
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0], # D
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 0], # E
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 1], # F
        [1, 1, 1, 0, 0, 0, 0, 1, 1, 0], # G
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0], # H
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0], # I
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0]  # J
    ]
    
    # Load and display unweighted map
    tool_unweighted.load_city_map(directed_unweighted_matrix)
    tool_unweighted.print_adjacency_matrix()
    tool_unweighted.display_city_map()

    tool_weighted = DisasterManagementTool(graph_type="directed_weighted")
    
    directed_weighted_matrix = [
        #A, B, C, D, E, F, G, H, I, J
        [0, 20, 5, 7, 7, 15, 25, 6, 23],   # A
        [20, 0, 34, 25, 15, 10, 4, 7, 16], # B
        [5, 34, 0, 20, 27, 10, 8, 12, 15], # C
        [7, 25, 20, 0, 3, 8, 9, 20, 7],    # D
        [7, 15, 27, 3, 0, 27, 23, 25, 0],  # E
        [15, 10, 10, 8, 27, 0, 3, 7, 21],  # F
        [25, 4, 8, 9, 23, 3, 0, 17, 6],    # G
        [6, 7, 12, 20, 25, 7, 17, 0, 30],  # H
        [23, 16, 15, 7, 5, 21, 6, 30, 0]   # I
    ]
    
    tool_weighted.load_city_map(directed_weighted_matrix)
    tool_weighted.print_adjacency_matrix()
    tool_weighted.display_city_map()
    
    tool_weighted = DisasterManagementTool(graph_type="undirected_unweighted")
    
    undirected_unweighted_matrix = [
        #A, B, C, D, E, F, G, H, I, J
        [0, 1, 1, 1, 0, 0, 1, 0, 0, 1], # A
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 0], # B
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 0], # C
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 0], # D
        [0, 1, 0, 0, 0, 1, 0, 1, 0, 0], # E
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 0], # F
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 0], # G
        [0, 0, 0, 1, 1, 0, 0, 0, 1, 0], # H
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 1], # I
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0]  # J
    ]
    
    tool_weighted.load_city_map(undirected_unweighted_matrix)
    tool_weighted.print_adjacency_matrix()
    tool_weighted.display_city_map()
    
    
    tool_weighted = DisasterManagementTool(graph_type="undirected_weighted")
    
    undirected_weighted_matrix = [
        #A, B, C, D, E, F, G, H, I, J
        [0, 1, 1, 1, 0, 0, 1, 0, 0, 1],     # A
        [1, 0, 0, 0, 6, 2, 8, 0, 0, 0],     # B
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 0],     # C
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 0],     # D
        [0, 6, 0, 0, 0, 1, 0, 13, 0, 0],    # E
        [0, 2, 0, 0, 1, 0, 0, 0, 0, 0],     # F
        [1, 8, 1, 0, 0, 0, 0, 0, 2, 0],     # G
        [0, 0, 0, 1, 13, 0, 0, 0, 9, 0],    # H
        [0, 0, 0, 0, 0, 0, 2, 9, 0, 2],     # I
        [1, 0, 0, 0, 0, 0, 0, 0, 2, 0]      # J
    ]
    
    tool_weighted.load_city_map(undirected_weighted_matrix)
    tool_weighted.print_adjacency_matrix()
    tool_weighted.display_city_map()
