import numpy as np


def classify_terrain(points, height_threshold=0.15, flatness_threshold=0.05):
    """
    Simple rule-based terrain classifier.
    Classifies each point as 'drivable' (road) or 'non-drivable' (obstacle/curb/pothole).
    
    Logic: points close to ground level (low height) and relatively flat
    compared to their neighbors are considered drivable.
    
    Args:
        points: array of shape (N, 4) -> x, y, z, intensity (already aligned to vehicle frame)
        height_threshold: max height (in meters) above ground to still count as drivable
        flatness_threshold: not used in this simple version, reserved for future improvement
    
    Returns:
        labels: array of shape (N,) with values 'drivable' or 'non_drivable'
    """
    z = points[:, 2]
    
    labels = np.where(z <= height_threshold, "drivable", "non_drivable")
    
    return labels


if __name__ == "__main__":
    from src.preprocessing.loader import generate_fake_point_cloud
    from src.preprocessing.filters import remove_outliers, downsample
    from src.preprocessing.alignment import align_to_vehicle_frame

    points = generate_fake_point_cloud(num_points=1000)
    points = remove_outliers(points, max_distance=60.0)
    points = align_to_vehicle_frame(points)

    labels = classify_terrain(points)

    drivable_count = np.sum(labels == "drivable")
    non_drivable_count = np.sum(labels == "non_drivable")

    print(f"Total points: {len(points)}")
    print(f"Drivable points: {drivable_count}")
    print(f"Non-drivable points: {non_drivable_count}")