import numpy as np
from src.grid_engine.quadtree import VariableResolutionGrid
from src.grid_engine.resolution_config import RESOLUTION_ZONES


def project_points_to_grid(points, final_labels):
    """
    Projects a full labeled point cloud into the variable-resolution grid.
    This is the bridge between the fusion module's output and the grid engine.
    
    Args:
        points: array of shape (N, 4) -> x, y, z, intensity
        final_labels: array of shape (N,) -> output from fuse_labels()
    
    Returns:
        grid: a populated VariableResolutionGrid object
    """
    grid = VariableResolutionGrid(RESOLUTION_ZONES)
    
    for i in range(len(points)):
        x, y, z = points[i, 0], points[i, 1], points[i, 2]
        label = final_labels[i]
        grid.add_point(x, y, z, label)
    
    return grid


if __name__ == "__main__":
    from src.preprocessing.loader import generate_fake_point_cloud
    from src.preprocessing.filters import remove_outliers
    from src.preprocessing.alignment import align_to_vehicle_frame
    from src.terrain_analysis.model import classify_terrain
    from src.object_detection.model import classify_objects
    from src.fusion.label_fusion import fuse_labels

    # Full pipeline, start to finish
    points = generate_fake_point_cloud(num_points=5000)
    points = remove_outliers(points, max_distance=90.0)
    points = align_to_vehicle_frame(points)

    terrain_labels = classify_terrain(points)
    object_labels = classify_objects(points, terrain_labels)
    final_labels = fuse_labels(terrain_labels, object_labels)

    grid = project_points_to_grid(points, final_labels)

    print(f"Input points: {len(points)}")
    print(f"Grid cells created: {grid.get_cell_count()}")
    print(f"Estimated grid memory: {grid.get_memory_estimate_bytes()} bytes")

    # Compare to a naive "one cell per point at finest resolution" estimate
    naive_memory = len(points) * 64
    print(f"Naive uniform-resolution memory estimate: {naive_memory} bytes")
    
    if naive_memory > 0:
        savings_pct = (1 - grid.get_memory_estimate_bytes() / naive_memory) * 100
        print(f"Memory savings: {savings_pct:.1f}%")