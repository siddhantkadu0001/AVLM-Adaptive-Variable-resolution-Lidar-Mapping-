import numpy as np


def classify_objects(points, terrain_labels, height_static_threshold=1.0):
    """
    Simple rule-based object classifier.
    Only classifies points already marked as 'non_drivable' by terrain analysis.
    
    Logic:
    - Tall points (above height_static_threshold) are likely static (walls, poles)
    - Shorter non-drivable points are treated as potential dynamic objects
      (pedestrians, vehicles) - in real data this would use motion across frames,
      but for now we use height as a simple placeholder heuristic.
    
    Args:
        points: array of shape (N, 4) -> x, y, z, intensity
        terrain_labels: array of shape (N,) with 'drivable'/'non_drivable' from terrain_analysis
        height_static_threshold: height (meters) above which we assume static structure
    
    Returns:
        object_labels: array of shape (N,) with values:
                        'none' (drivable, not an object),
                        'static' (wall/pole),
                        'dynamic' (pedestrian/vehicle)
    """
    z = points[:, 2]
    object_labels = np.full(len(points), "none", dtype=object)
    
    non_drivable_mask = terrain_labels == "non_drivable"
    
    static_mask = non_drivable_mask & (z > height_static_threshold)
    dynamic_mask = non_drivable_mask & (z <= height_static_threshold)
    
    object_labels[static_mask] = "static"
    object_labels[dynamic_mask] = "dynamic"
    
    return object_labels


if __name__ == "__main__":
    from src.preprocessing.loader import generate_fake_point_cloud
    from src.preprocessing.filters import remove_outliers
    from src.preprocessing.alignment import align_to_vehicle_frame
    from src.terrain_analysis.model import classify_terrain

    points = generate_fake_point_cloud(num_points=1000)
    points = remove_outliers(points, max_distance=60.0)
    points = align_to_vehicle_frame(points)

    terrain_labels = classify_terrain(points)
    object_labels = classify_objects(points, terrain_labels)

    static_count = np.sum(object_labels == "static")
    dynamic_count = np.sum(object_labels == "dynamic")
    none_count = np.sum(object_labels == "none")

    print(f"Total points: {len(points)}")
    print(f"Static objects: {static_count}")
    print(f"Dynamic objects: {dynamic_count}")
    print(f"None (drivable): {none_count}")