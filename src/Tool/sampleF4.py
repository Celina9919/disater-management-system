import numpy as np
import matplotlib.pyplot as plt
import random

# Input data: Deployment locations with coordinates
deployment_locations = {
    'A': (2, 3),  # Example coordinates for deployment locations
    'B': (5, 4),
    'C': (1, 7),
    'D': (8, 1),
    'E': (6, 5),
    'F': (7, 2)
}

waterways = {  # Optional waterway routes with distances
    ('A', 'B'): 3,
    ('C', 'D'): 4,
}

# Parameters
k = 2  # Number of additional supply points
coordinates = np.array(list(deployment_locations.values()))
location_names = list(deployment_locations.keys())

# Initialize centroids randomly from the data points
random.seed(42)  # For reproducibility
centroids = coordinates[random.sample(range(len(coordinates)), k)]

# K-Means Implementation
def kmeans_clustering(data, k, centroids, max_iterations=100, tolerance=1e-4):
    for iteration in range(max_iterations):
        # Step 1: Assign points to the nearest centroid
        clusters = {i: [] for i in range(k)}
        for point in data:
            distances = [np.linalg.norm(point - centroid) for centroid in centroids]
            cluster_idx = np.argmin(distances)
            clusters[cluster_idx].append(point)

        # Step 2: Recalculate centroids
        new_centroids = []
        for i in range(k):
            if clusters[i]:  # Avoid empty clusters
                new_centroids.append(np.mean(clusters[i], axis=0))
            else:
                # Randomly reinitialize the centroid if a cluster is empty
                new_centroids.append(data[random.randint(0, len(data) - 1)])
        new_centroids = np.array(new_centroids)

        # Step 3: Check for convergence
        shift = np.linalg.norm(new_centroids - centroids)
        if shift < tolerance:
            break

        centroids = new_centroids

    return centroids, clusters

# Perform clustering
final_centroids, clusters = kmeans_clustering(coordinates, k, centroids)

# Display results
print(f"Cluster Centers (Supply Points): {final_centroids}")
for cluster_idx, points in clusters.items():
    assigned_locations = [location_names[np.where((coordinates == point).all(axis=1))[0][0]] for point in points]
    print(f"Cluster {cluster_idx}: {assigned_locations}")

# Visualization
plt.figure(figsize=(10, 8))

# Plot deployment locations
for name, (x, y) in deployment_locations.items():
    plt.scatter(x, y, label=name, s=100)
    plt.text(x + 0.2, y, name, fontsize=10, color='black')

# Plot cluster centers (supply points)
for i, (x, y) in enumerate(final_centroids):
    plt.scatter(x, y, label=f"Supply Point {i}", s=200, marker='X')

# Draw waterway routes (optional)
for (start, end), distance in waterways.items():
    start_coord = deployment_locations[start]
    end_coord = deployment_locations[end]
    plt.plot(
        [start_coord[0], end_coord[0]],
        [start_coord[1], end_coord[1]],
        color='blue',
        linestyle='--',
        label=f"Waterway ({start}-{end})"
    )

plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.legend()
plt.title("Optimal Locations for Supply Points")
plt.grid()
plt.show()
