import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class DisasterManagementTool:
    def __init__(self):
        """Initialize an empty city map."""
        self.city_map = None  #will be loaded later
        self.node_labels = []  #store names of nodes (A,B,C) #empty list for initialising
        
    def load_city_map(self, adjacency_matrix, node_labels=None): 
        #define method 
        #adjacency_matrix : square qrid for the matrix
        #node_labels A,B,C
        
        """Load a city map from an adjacency matrix."""
        self.city_map = np.array(adjacency_matrix)
        #converts adjacency_matrix into numpy array
        
        self.node_labels = node_labels if node_labels else [chr(65 + i) for i in range(len(adjacency_matrix))]
        #chr(65+i) creates character, 65 is A.. chr 65+1 is B
        #IF NO NODES GIVEN, THIS FUNCTION GIVES LABELS
        print("City map loaded successfully.")
        
    def display_city_map(self):
        """Display the city map as a graph using NetworkX and Matplotlib."""
        if self.city_map is None:
            print("No city map loaded.")
            return
        
        
        G = nx.Graph()  #networkX creates empty graph first
        for i, node in enumerate(self.node_labels): #loop goes through nodes, for every i it gives node labels, i acts like a pointer
            G.add_node(node) #adds node to the graph , adding anew city location to the map

        for i in range(len(self.city_map)): #loop goes through each row (each node)
            for j in range(i + 1, len(self.city_map[i])):  # loop goes through each column --> Avoid duplicating edges(A-B, B-A)
                if self.city_map[i][j] != 0:  # Edge(road) exists if not 0
                    G.add_edge(self.node_labels[i], self.node_labels[j], weight=self.city_map[i][j])
                    #adds edge(road) between 2 nodes(places) in graph
                    #weight = distance btw places
                    #self.city_map[i][j] = road’s distance (from adjacency matrix)

        pos = nx.spring_layout(G)  # the looks for the graph
        nx.draw(G, 
                pos, 
                with_labels=True, 
                node_color='lightblue', 
                edge_color='gray', 
                node_size=1500, 
                font_size=12) #draws graph
        edge_labels = nx.get_edge_attributes(G, 'weight') #gets weights of edges
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) #draw the weights on graph
        plt.title("City Map of Schilda")
        plt.show()

        