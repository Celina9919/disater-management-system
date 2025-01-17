import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class DisasterManagementTool:
    def __init__(self, graph_type="directed_unweighted"):
        """Initialize the disaster management tool."""
        self.city_map = None  # Adjacency matrix for the city map
        self.node_labels = []  # Names of the nodes
        self.graph_type = graph_type  # Type of graph (directed, undirected, weighted, unweighted)
        self.important_points = {}  # Dictionary of important points and their details
        self.impassable_roads = []  # List of impassable roads
        self.road_types = {}  # Dictionary of road types (land, waterway)

    def load_city_map(self, adjacency_matrix, node_labels=None):
        """Load a city map from an adjacency matrix."""
        self.city_map = np.array(adjacency_matrix)  # Convert adjacency matrix to a NumPy array
        self.node_labels = node_labels if node_labels else [chr(65 + i) for i in range(len(adjacency_matrix))]
        print(f"{self.graph_type.capitalize()} city map loaded successfully.")

    def print_adjacency_matrix(self):
        """Print the adjacency matrix of the city map."""
        if self.city_map is None:
            print("No city map loaded.")
            return
        print(f"\nAdjacency Matrix ({self.graph_type.capitalize()}):")
        print("   ", " ".join(self.node_labels))
        for i, row in enumerate(self.city_map):
            print(f"{self.node_labels[i]}  ", " ".join(map(str, row)))


###########B2 FUNCTIONS STARTS HERE############ 
    def add_important_point(self, name, location, distance=None):
        """Add an important point to the city map."""
        self.important_points[name] = (location, distance)
        print(f"Important point '{name}' added at location '{location}' with distance {distance}m.")

    def mark_road_impassable(self, start, end):
        """Mark a road as impassable."""
        if (start, end) not in self.impassable_roads:
            self.impassable_roads.append((start, end))
            print(f"Road from {start} to {end} marked as impassable.")

    def add_road_type(self, start, end, road_type):
        """Specify the type of a road (land or waterway)."""
        if road_type not in ['land', 'waterway']:
            print("Invalid road type. Must be 'land' or 'waterway'.")
            return
        self.road_types[(start, end)] = road_type
        print(f"Road from {start} to {end} set as {road_type}.")

    
    ########GRAPH DISPLAYING##########
    
    def display_city_map(self):
        """Display the city map with all features."""
        if self.city_map is None:
            print("No city map loaded.")
            return

        # Initialize the graph
        G = nx.Graph() if "directed" in self.graph_type else nx.Graph()

        # Add nodes and edges
        for node in self.node_labels:
            G.add_node(node)
        for i in range(len(self.city_map)):
            for j in range(len(self.city_map[i])):
                if self.city_map[i][j] != 0:
                    weight = self.city_map[i][j] if "weighted" in self.graph_type else None
                    if (self.node_labels[i], self.node_labels[j]) not in self.impassable_roads:
                        G.add_edge(self.node_labels[i], self.node_labels[j], weight=weight)

        # Set up graph layout
        pos = nx.spring_layout(G, k=2.5)
        plt.figure(figsize=(10, 8))

        # Assign edge colors based on road types and impassable status
        edge_colors = []
        for u, v in G.edges():
            if (u, v) in self.impassable_roads or (v, u) in self.impassable_roads:
                edge_colors.append('red')  # Impassable roads
            elif self.road_types.get((u, v)) == 'waterway':
                edge_colors.append('blue')  # Waterways
            else:
                edge_colors.append('gray')  # Normal roads

        # Draw the graph
        nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', edge_color=edge_colors,
                         node_size=1500, font_size=12, arrows=True)
        if "weighted" in self.graph_type:
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Add important points
        for point, (location, distance) in self.important_points.items():
            plt.text(pos[location][0], pos[location][1] + 0.1,
                     f"{point} ({distance}m)" if distance else point,
                     fontsize=10, fontweight='bold', color='darkred')

        # Display the final map
        plt.title("City Map with Roads and Features")
        plt.show()


if __name__ == "__main__":
    
    tool = DisasterManagementTool(graph_type="undirected_weighted")

    node_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    test_matrix = [
        [0, 20, 5, 7, 7, 15, 25, 6, 23],
        [20, 0, 34, 25, 15, 10, 4, 7, 16],
        [5, 34, 0, 20, 27, 10, 8, 12, 15],
        [7, 25, 20, 0, 3, 8, 9, 20, 7],
        [7, 15, 27, 3, 0, 27, 23, 25, 0],
        [15, 10, 10, 8, 27, 0, 3, 7, 21],
        [25, 4, 8, 9, 23, 3, 0, 17, 6],
        [6, 7, 12, 20, 25, 7, 17, 0, 30],
        [23, 16, 15, 7, 5, 21, 6, 30, 0]
    ]

    # Load city map
    tool.load_city_map(test_matrix, node_labels)
    tool.print_adjacency_matrix()

    # Add important points
    tool.add_important_point("Hospital", "A", 200)
    tool.add_important_point("Government Building", "C", 150)

    # Mark roads and set road types
    tool.mark_road_impassable("F", "E")
    tool.add_road_type("A", "B", "land")
    tool.add_road_type("E", "I", "waterway")

    # Display the final city map
    tool.display_city_map()
