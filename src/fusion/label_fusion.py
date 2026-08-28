import numpy as np


def fuse_labels(terrain_labels, object_labels):
    """
    Merges terrain labels and object labels into one final label per point.
    
    Priority rule: if a point is classified as an object (static/dynamic),
    that takes priority over terrain classification, since obstacles matter
    more for safety than terrain type.
    
    Args:
        terrain_labels: array of shape (N,) -> 'drivable' / 'non_drivable'
        object_labels: array of shape (N,) -> 'none' / 'static' / 'dynamic'
    
    Returns:
        final_labels: array of shape (N,) with one of:
                       'drivable', 'static_obstacle', 'dynamic_object'
    """
    final_labels = np.full(len(terrain_labels), "drivable", dtype=object)
    
    # Default: use terrain label first
    final_labels[terrain_labels == "non_drivable"] = "non_drivable"
    
    # Object labels override terrain where applicable
    final_labels[object_labels == "static"] = "static_obstacle"
    final_labels[object_labels == "dynamic"] = "dynamic_object"
    
    return final_labels


if __name__ == "__main__":
    from src.preprocessing.loader import generate_fake_point_cloud
    from src.preprocessing.filters import remove_outliers
    from src.preprocessing.alignment import align_to_vehicle_frame
    from src.terrain_analysis.model import classify_terrain
    from src.object_detection.model import classify_objects

    points = generate_fake_point_cloud(num_points=1000)
    points = remove_outliers(points, max_distance=60.0)
    points = align_to_vehicle_frame(points)

    terrain_labels = classify_terrain(points)
    object_labels = classify_objects(points, terrain_labels)

    final_labels = fuse_labels(terrain_labels, object_labels)

    unique, counts = np.unique(final_labels, return_counts=True)
    print(f"Total points: {len(points)}")
    for label, count in zip(unique, counts):
        print(f"{label}: {count}")