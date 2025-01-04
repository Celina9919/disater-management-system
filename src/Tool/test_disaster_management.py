from BasicFunctions import DisasterManagementTool

node_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

def test_graph(adjacency_matrix, graph_type):
    tool = DisasterManagementTool(graph_type)
    tool.load_city_map(adjacency_matrix, node_labels)
    tool.print_adjacency_matrix()
    tool.display_city_map()  # ensure called only once here
    

def add_new_features(tool):
    """Adds important points, impassable roads, and road types to each graph tool."""
    
    tool.add_important_point('Supply Depot 1', 'A', distance=50)
    tool.add_important_point('Evacuation Point', 'C')
    
    tool.mark_road_impassable('B', 'C')

    tool.add_road_type('E', 'I', 'waterway')


###############################

if __name__ == "__main__":
    # Example input from prof
    # Example input adjacency matrix of directed unweighted graph with self-loops
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
    
    # Test the different adjacency matrices
    tool = DisasterManagementTool("directed_unweighted")
    tool.load_city_map(directed_unweighted_matrix, node_labels)
    add_new_features(tool)  
    tool.print_adjacency_matrix()
    tool.display_city_map()

    # Other matrices to test
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
    
    # Test other matrices
    test_graph(directed_weighted_matrix, "directed_weighted")
    #test_graph(undirected_unweighted_matrix, "undirected_unweighted")
    #test_graph(undirected_weighted_matrix, "undirected_weighted")
