import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import heapq  # For Dijkstra's algorithm

# Function to parse the adjacency matrix into an adjacency list
def parse_to_adjacency_list(lines):
    node_labels = lines[0].strip().split()
    matrix = [list(map(int, line.strip().split()[1:])) for line in lines[1:]]
    graph = {label: {} for label in node_labels}
    
    for i, node1 in enumerate(node_labels):
        for j, node2 in enumerate(node_labels):
            if matrix[i][j] > 0:
                graph[node1][node2] = matrix[i][j]
    
    return graph

# Function to implement Dijkstra's algorithm
def dijkstra(graph, start_node):
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    predecessors = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, predecessors

# Function to visualize the graph with shortest paths
def visualize_graph(graph, distances, predecessors, start_node):
    G_visual = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G_visual.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G_visual)  # Spring layout for better visualization
    nx.draw(G_visual, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    edge_labels = nx.get_edge_attributes(G_visual, 'weight')
    nx.draw_networkx_edge_labels(G_visual, pos, edge_labels=edge_labels)

    # Highlight the shortest paths from the start node
    for node, distance in distances.items():
        if node != start_node and predecessors[node] is not None:
            path = []
            current = node
            while current:
                path.append(current)
                current = predecessors[current]
            path.reverse()
            nx.draw_networkx_edges(
                G_visual, pos,
                edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)],
                width=2.5, edge_color='red'
            )

    plt.title(f"Graph Visualization with Shortest Paths from Node {start_node}")
    plt.show()

# Main Execution
with open('D:/Programming Java/algodata/src/Data/undirected_weighted_graph.txt', 'r') as f:
    lines = [line for line in f if line.strip()]

graph = parse_to_adjacency_list(lines)

# Start node for Dijkstra
start_node = 'E'
distances_from_e, predecessors_from_e = dijkstra(graph, start_node)

# Display distances and predecessors as DataFrame
results_from_e_df = pd.DataFrame({
    "Node": distances_from_e.keys(),
    "Shortest Distance from E": distances_from_e.values(),
    "Predecessor": [predecessors_from_e[node] for node in distances_from_e.keys()]
})
print(results_from_e_df)  # Print to console

# Visualize the graph
visualize_graph(graph, distances_from_e, predecessors_from_e, start_node)


