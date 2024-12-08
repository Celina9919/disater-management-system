from DisasterManagementTool import DisasterManagementTool

if __name__ == "__main__":
    # example input from prof
    # Adjacency matrix of directed_uweighted graph
    adjacency_matrix = [
        [0, 1, 0, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 1, 1, 0, 0],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    ]

    # Define node labels
    node_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    # initialise
    tool = DisasterManagementTool()
    
    # load and display city map
    tool.load_city_map(adjacency_matrix, node_labels)
    tool.print_adjacency_matrix()
    tool.display_city_map()
    

