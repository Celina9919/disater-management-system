"""
Use Maximum Flow Algorithms (specifically, the Edmonds-Karp Algorithm,
Edmonds-Karp algorithm uses Breadth First Search (BFS) to find augmented paths to increase flow) to determine
whether the existing infrastructure can handle the evacuation demand
from assembly points to emergency shelters, considering road and water routes.

The Edmonds-Karp algorithm works by using Breadth-First Search (BFS)
to find a path with available capacity from the source to the sink (called an augmented path),
and then sends as much flow as possible through that path.

The Edmonds-Karp algorithm continues to find new paths to send more flow through until the maximum flow is reached.
"""

import pandas as pd
import networkx as nx

# Input data
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

shelters = {
    'A': 200,  # Hospital shelter 200 people
    'B': 150,  # Rescue Station shelter 150 people
    'C': 250,  # Government Building shelter 250 people
    'D': 50,  # Evacuation Point shelter 50 people

}

evacuation_needs = {
    'D': 300  #500 ppl need to ecavuate
}

# Create the graph with capacities
city_map = nx.DiGraph()

# Add assembly points to the graph with edges to a source node
city_map.add_node('Source')
for point, people in evacuation_needs.items():
    city_map.add_edge('Source', point, capacity=people)

# Add shelters to the graph with edges from a sink node
city_map.add_node('Sink')
for shelter, capacity in shelters.items():
    city_map.add_edge(shelter, 'Sink', capacity=capacity)

# Add intermediate routes with capacities
routes = {
    ('A', 'X'): 25,  # Example: Route from A to X can handle 25 people
    ('A', 'Y'): 15,  # Example: Route from A to Y can handle 15 people
    ('B', 'X'): 10,  # Example: Route from B to X can handle 10 people
    ('B', 'Y'): 20,  # Example: Route from B to Y can handle 20 people
    ('C', 'X'): 20,  # Example: Route from C to X can handle 20 people
    ('C', 'Y'): 30   # Example: Route from C to Y can handle 30 people
}
for (start, end), capacity in routes.items():
    city_map.add_edge(start, end, capacity=capacity)

# Add waterway routes (optional)
waterway_routes = {
    ('C', 'X'): 10  # Example: Additional capacity over water from C to X
}
for (start, end), capacity in waterway_routes.items():
    city_map.add_edge(start, end, capacity=capacity)

# Calculate the maximum flow
flow_value, flow_dict = nx.maximum_flow(city_map, 'Source', 'Sink')

# Output results
print(f"Maximum Flow: {flow_value}")
print("Flow Details:")
for source, targets in flow_dict.items():
    for target, flow in targets.items():
        if flow > 0:
            print(f"  {source} -> {target}: {flow}")

# Decision based on the flow
total_demand = sum(assembly_points.values())
if flow_value >= total_demand:
    print("The existing infrastructure is sufficient for evacuation.")
else:
    print("Additional infrastructure is needed for evacuation.")
