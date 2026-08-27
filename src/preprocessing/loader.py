import numpy as np


def generate_fake_point_cloud(num_points=1000):
    """
    Generates a fake Lidar point cloud for testing purposes.
    Each point has: x, y, z, intensity
    
    This lets us test our pipeline without needing to download
    real Lidar data yet.
    """
    # Random points spread out in a 100m x 100m area around the sensor
    x = np.random.uniform(-50, 50, num_points)
    y = np.random.uniform(-50, 50, num_points)
    z = np.random.uniform(-2, 3, num_points)  # height range
    intensity = np.random.uniform(0, 1, num_points)

    points = np.stack([x, y, z, intensity], axis=1)
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