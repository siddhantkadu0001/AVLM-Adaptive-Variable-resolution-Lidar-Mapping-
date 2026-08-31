import numpy as np


def generate_fake_point_cloud(num_points=5000):
    """
    Generates a more realistic fake Lidar point cloud for testing.
    Simulates a road scene: dense ground plane near the vehicle,
    a few obstacles at various distances, and sparser points far away
    (similar to how real Lidar data is naturally distributed).
    """
    if num_points <= 0:
        print("Warning: num_points must be positive, defaulting to 100")
        num_points = 100
    points_list = []

    # 1. Ground plane points - dense, spread across full range, low height
    num_ground = int(num_points * 0.7)
    ground_x = np.random.uniform(-80, 80, num_ground)
    ground_y = np.random.uniform(-80, 80, num_ground)
    ground_z = np.random.uniform(-0.05, 0.05, num_ground)  # flat, near z=0
    ground_intensity = np.random.uniform(0.3, 0.6, num_ground)
    ground_points = np.stack([ground_x, ground_y, ground_z, ground_intensity], axis=1)
    points_list.append(ground_points)

    # 2. Static obstacles (walls, poles) - tall, clustered at a few locations
    num_static = int(num_points * 0.15)
    num_clusters = 5
    for _ in range(num_clusters):
        cluster_center_x = np.random.uniform(-70, 70)
        cluster_center_y = np.random.uniform(-70, 70)
        cluster_size = num_static // num_clusters
        cx = cluster_center_x + np.random.normal(0, 0.5, cluster_size)
        cy = cluster_center_y + np.random.normal(0, 0.5, cluster_size)
        cz = np.random.uniform(1.0, 3.0, cluster_size)  # tall
        cintensity = np.random.uniform(0.5, 0.9, cluster_size)
        cluster_points = np.stack([cx, cy, cz, cintensity], axis=1)
        points_list.append(cluster_points)

    # 3. Dynamic objects (pedestrians, vehicles) - clustered, medium height
    num_dynamic = num_points - num_ground - (num_static // num_clusters) * num_clusters
    num_dyn_clusters = 3
    for _ in range(num_dyn_clusters):
        cluster_center_x = np.random.uniform(-50, 50)
        cluster_center_y = np.random.uniform(-50, 50)
        cluster_size = max(num_dynamic // num_dyn_clusters, 1)
        cx = cluster_center_x + np.random.normal(0, 0.3, cluster_size)
        cy = cluster_center_y + np.random.normal(0, 0.3, cluster_size)
        cz = np.random.uniform(0.3, 0.9, cluster_size)  # human/vehicle height
        cintensity = np.random.uniform(0.4, 0.7, cluster_size)
        cluster_points = np.stack([cx, cy, cz, cintensity], axis=1)
        points_list.append(cluster_points)

    points = np.vstack(points_list)
    np.random.shuffle(points)  # mix everything together, like a real scan
    return points


def load_point_cloud(file_path):
    """
    Loads a real point cloud file (.bin format, used by SemanticKITTI).
    Returns a numpy array of shape (N, 4) -> x, y, z, intensity
    """
    points = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
    return points


if __name__ == "__main__":
    # Test with fake data first
    points = generate_fake_point_cloud(num_points=1000)
    print(f"Generated {points.shape[0]} fake points")
    print(f"Sample point (x, y, z, intensity): {points[0]}")
    print(f"Point cloud shape: {points.shape}")