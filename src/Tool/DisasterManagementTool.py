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
        
        
    

     
        