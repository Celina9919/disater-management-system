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
assembly_points = {
    'A': 30,  # Example: Node A has 30 people to evacuate
    'B': 20,  # Example: Node B has 20 people to evacuate
    'C': 50   # Example: Node C has 50 people to evacuate
}
shelters = {
    'X': 50,  # Example: Shelter X can accommodate 40 people
    'Y': 60   # Example: Shelter Y can accommodate 60 people
}

# Create the graph with capacities
city_map = nx.DiGraph()

# Add assembly points to the graph with edges to a source node
city_map.add_node('Source')
for point, capacity in assembly_points.items():
    city_map.add_edge('Source', point, capacity=capacity)

# Add shelters to the graph with edges from a sink node
city_map.add_node('Sink')
for shelter, capacity in shelters.items():
    city_map.add_edge(shelter, 'Sink', capacity=capacity)

# Add intermediate routes with capacities
routes = {
    ('A', 'X'): 20,  # Example: Route from A to X can handle 25 people
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
