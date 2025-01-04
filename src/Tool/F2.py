import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

file_path = 'src/Data/undirected_weighted_graph.txt'
adjacency_matrix = pd.read_csv(file_path, delim_whitespace=True, index_col=0)

G = nx.Graph()

# same but + capacities for infrastructure (e.g., buses, boats)
for i, row in adjacency_matrix.iterrows():
    for j, weight in row.items():
        if weight > 0 and i != j:  # ignore 0s n self-loops
            # Here : assume a capacity for each edge (example: 100 people per hour)
            # eg : road capacities, bus capacities, or boat capacities
            capacity = 100  # set default capacity, can be adjusted for each edge if needed
            G.add_edge(i, j, weight=weight, capacity=capacity)

node_attributes = {
    'A': "Hospital",
    'B': "Rescue Station",
    'C': "Government Building",
    'D': "Evacuation Point",
    'E': "Boat Rescue",
    'F': "Emergency Service",
    'G': "Supply Point",
    'H': "Staging Area",
    'I': "Staging Area"
}
nx.set_node_attributes(G, node_attributes, "description")

####### NUM OF PPL NEED TO EVACUATE
evacuation_needs = {
    'D': 500,  # Evacuation D : 500 people to evacuate
}

shelters = ['A', 'B', 'C', 'G', 'H', 'I']  

for u, v in G.edges():
    if ('E' in {u, v}) and ('I' in {u, v}):
        G.edges[u, v]["type"] = "Waterway"
        G.edges[u, v]["color"] = "blue"
    else:
        G.edges[u, v]["color"] = "lightgray"
        G.edges[u, v]["type"] = " "

# DJIKSTRA FUNCTION
def evacuation_routes_dijkstra(evacuation_points, shelters, G):
    # dict : shortest route n lengths
    evacuation_plans = {}

    # for EACH evacuation point
    for evac_point in evacuation_points:
        ###### DJIKSTRA ALGO
        shortest_paths = {}
        for shelter in shelters:
            try:
                path_length = nx.dijkstra_path_length(G, source=evac_point, target=shelter, weight='weight')
                path = nx.dijkstra_path(G, source=evac_point, target=shelter, weight='weight')
                shortest_paths[shelter] = (path, path_length)
            except nx.NetworkXNoPath:
                shortest_paths[shelter] = ("No path", float('inf'))  # no path from one node to the other!!
        
        evacuation_plans[evac_point] = shortest_paths

    return evacuation_plans


# evacuation_routes function = calculate the evacuation plans
evacuation_plans = evacuation_routes_dijkstra(evacuation_points, shelters, G)

# evacuation routes and their lengths 4 each evacuation point
for evac_point, routes in evacuation_plans.items():
    print(f"Evacuation Routes from {evac_point}:")
    for shelter, (path, length) in routes.items():
        print(f"  To Shelter {shelter}: Path = {path}, Length = {length}")
        
def save_evacuation_plans_to_csv(evacuation_plans, filename='evacuation_plans.csv'):
    # Prepare data for CSV
    data = []
    for evac_point, routes in evacuation_plans.items():
        for shelter, (path, length) in routes.items():
            # Flatten the path list to a string (e.g., 'D -> B -> A')
            path_str = ' -> '.join(path) if isinstance(path, list) else path
            data.append([evac_point, shelter, path_str, length])
    
    # Convert data to a DataFrame
    df = pd.DataFrame(data, columns=['Evacuation Point', 'Shelter', 'Path', 'Path Length'])
    
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
    print(f"Evacuation plans have been saved to {filename}")
    
    # Save evacuation plans to a CSV file
save_evacuation_plans_to_csv(evacuation_plans, 'evacuation_plans.csv')


def visualize_evacuations(evacuation_plans, G):
    pos = nx.spring_layout(G, seed=42) 
    plt.figure(figsize=(10, 10))
    
    node_labels = {node: f"{node}: {data['description']}" for node, data in G.nodes(data=True)}
    edge_labels = {(u, v): f"{data['type']} ({data.get('weight', 0)})" for u, v, data in G.edges(data=True)}


    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="rosybrown")
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_color="navy", font_weight="bold", font_family="monospace")

    # evacuation paths in pink
    for evac_point, routes in evacuation_plans.items():
        for shelter, (path, _) in routes.items():
            edge_list = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='pink', width=2)
            
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="black", font_family="monospace")
    
    # labelling waterway 
    edge_labels = {}
    for u, v, data in G.edges(data=True):
        label = data['type']
        if label == "Waterway":
            edge_labels[(u, v)] = f"Waterway ({data['weight']})"
        else:
            edge_labels[(u, v)] = f"{data.get('weight', 0)}"  
    

    #  all edges with their respective colors
    edge_colors = [data["color"] for _, _, data in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1)
    
    # add edge labels for attributes
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, font_color="black", font_family="monospace")

    plt.title("Evacuation Routes in Schilda City")
    plt.show()
    
visualize_evacuations(evacuation_plans, G)




