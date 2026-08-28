import numpy as np


def remove_outliers(points, max_distance=100.0):
    """
    Removes points that are unrealistically far away (likely sensor noise/errors).
    
    Args:
        points: array of shape (N, 4) -> x, y, z, intensity
        max_distance: maximum allowed distance from sensor (in meters)
    
    Returns:
        Filtered array with outliers removed
    """
    distances = np.sqrt(points[:, 0]**2 + points[:, 1]**2)
    mask = distances <= max_distance
    filtered_points = points[mask]
    return filtered_points


#--------------------------------------------------------------------------------------------------------

def downsample(points, keep_ratio=0.5):
    """
    Reduces the number of points by randomly keeping only a fraction of them.
    Useful when point clouds are too dense to process in real-time.
    
    Args:
        points: array of shape (N, 4)
        keep_ratio: fraction of points to keep (0.5 = keep half)
    
    Returns:
        Downsampled array
    """
    num_points = points.shape[0]
    num_keep = int(num_points * keep_ratio)
    
    indices = np.random.choice(num_points, num_keep, replace=False)
    downsampled_points = points[indices]
    
    return downsampled_points


if __name__ == "__main__":
    # Quick test using fake data
    from loader import generate_fake_point_cloud

    points = generate_fake_point_cloud(num_points=1000)
    print(f"Original points: {points.shape[0]}")

    filtered = remove_outliers(points, max_distance=60.0)
    print(f"After outlier removal: {filtered.shape[0]}")

    downsampled = downsample(filtered, keep_ratio=0.5)
    print(f"After downsampling: {downsampled.shape[0]}")



