# Import the DisasterManagementTool class from the BasicFunctions module
from BasicFunctions import DisasterManagementTool

# Predefined labels for graph nodes
node_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']


def test_graph(adjacency_matrix, graph_type):
    """
    General function to test graph functionality.
    Args:
        adjacency_matrix (list of lists): The graph's adjacency matrix representation.
        graph_type (str): Type of the graph ('directed_unweighted', 'directed_weighted', etc.).
    """
    # Initialize the tool with the graph type
    tool = DisasterManagementTool(graph_type) 
    # Load the city map (graph) into the tool using the adjacency matrix and node labels
    tool.load_city_map(adjacency_matrix, node_labels)  
    tool.print_adjacency_matrix() # Print the adjacency matrix for visualization in the console
    tool.display_city_map()  # Display the graph visually, ensure called only once here
    
def add_new_features(tool):
    """Adds important points, impassable roads, and road types to each graph tool.
    Args:
        tool (DisasterManagementTool): The tool managing the graph."""

    tool.add_important_point('Supply Depot 1', 'A', distance=50) # Add a supply depot to node 'A'
    tool.add_important_point('Evacuation Point', 'C') # Add an evacuation point to node 'C'
    tool.mark_road_impassable('B', 'C') # Mark the road between nodes 'B' and 'C' as impassable
    tool.add_road_type('E', 'I', 'waterway') # Mark the road between 'E' and 'I' as a waterway


    
###############################
# Main script execution
if __name__ == "__main__":
    # Example test input provided
    # Example adjacency matrix of directed unweighted graph with self-loops
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
    

   # Example matrices for other graph types
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
    
    # Test the directed_unweighted_graph for basic function 1 (display graph)
    #test_graph(directed_unweighted_matrix, "directed_unweighted")
    
    

    # Test the directed_unweighted_graph for basic function 2 (modify and update graph)
    tool = DisasterManagementTool("directed_weighted") # Create an instance of the tool with a specific graph type
    tool.load_city_map(directed_weighted_matrix, node_labels) # Load the adjacency matrix into the tool
    add_new_features(tool)  # Add important points, impassable roads, and road types
    tool.print_adjacency_matrix() # Print the updated adjacency matrix
    tool.display_city_map() # Display the modified graph

    # Test other matrices by uncommenting these lines
    # test_graph(directed_weighted_matrix, "directed_weighted")
    # test_graph(undirected_unweighted_matrix, "undirected_unweighted")
    # test_graph(undirected_weighted_matrix, "undirected_weighted")


    