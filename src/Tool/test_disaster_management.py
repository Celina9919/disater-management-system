from DisasterManagementTool import DisasterManagementTool

if __name__ == "__main__":
    # example input from prof
    # Adjacency matrix of directed_uweighted graph
    adjacency_matrix = [
        #A #B #C #D #E #F #G #H #I #J
        [0, 1, 0, 0, 1, 0, 1, 1, 0, 1], #A
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0], #B
        [1, 0, 0, 1, 0, 0, 1, 1, 0, 0], #C
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0], #D
        [0, 1, 0, 0, 1, 1, 0, 0, 0, 0], #E
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 1], #F
        [1, 1, 1, 0, 0, 0, 0, 1, 1, 0], #G
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0], #H
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0], #I
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0]  #J
    ]

    # Define node labels
    node_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    # initialise
    tool = DisasterManagementTool()
    
    # load and display city map
    tool.load_city_map(adjacency_matrix, node_labels)
    tool.print_adjacency_matrix()
    tool.display_city_map()
    

