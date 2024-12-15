from BasicFunctions import DisasterManagementTool

node_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

def test_graph(adjacency_matrix, graph_type):
    tool = DisasterManagementTool(graph_type)
    tool.load_city_map(adjacency_matrix, node_labels)
    tool.print_adjacency_matrix()
    tool.display_city_map()  # Ensure it's called only once here

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
    test_graph(directed_unweighted_matrix, "directed_unweighted")

    # Other matrices to test
    directed_weighted_matrix = [
        #A, B, C, D, E, F, G, H, I, J
        [5, 1, 0, 1, 1, 0, 5, 25, 0, 17],   # A
        [15, 8, 4, 0, 1, 10, 0, 0, 0, 34],  # B
        [15, 0, 5, 1, 7, 0, 9, 1, 0, 0],    # C
        [6, 4, 1, 0, 1, 0, 0, 0, 0, 0],     # D
        [0, 1, 9, 0, 0, 10, 0, 0, 0, 0],    # E
        [0, 3, 0, 0, 5, 0, 0, 0, 0, 12],    # F
        [2, 3, 9, 0, 0, 0, 0, 7, 10, 0],    # G
        [8, 6, 15, 2, 2, 0, 0, 0, 0, 0],    # H
        [0, 13, 0, 0, 0, 0, 17, 34, 3, 0],  # I
        [9, 0, 3, 0, 0, 0, 0, 0, 23, 0]     # J
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
    test_graph(undirected_unweighted_matrix, "undirected_unweighted")
    test_graph(undirected_weighted_matrix, "undirected_weighted")
