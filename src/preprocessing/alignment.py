import numpy as np


def align_to_vehicle_frame(points, sensor_offset=(0.0, 0.0, 1.8)):
    """
    Aligns Lidar points to the vehicle's coordinate frame.
    
    Lidar sensors are usually mounted above the vehicle (not at ground level),
    so raw points are measured relative to the SENSOR position, not the ground.
    This function shifts points so they're measured relative to the VEHICLE
    (with z=0 being ground level), which is what our grid engine expects.
    
    Args:
        points: array of shape (N, 4) -> x, y, z, intensity
        sensor_offset: (x, y, z) offset of sensor from vehicle center/ground
                       default z=1.8m is a typical Lidar mounting height
    
    Returns:
        Aligned points array, same shape
    """
    aligned_points = points.copy()
    aligned_points[:, 0] -= sensor_offset[0]  # x offset
    aligned_points[:, 1] -= sensor_offset[1]  # y offset
    aligned_points[:, 2] += sensor_offset[2]  # z offset (sensor is above ground)
    
    return aligned_points


if __name__ == "__main__":
    from loader import generate_fake_point_cloud

    points = generate_fake_point_cloud(num_points=10)
    print("Before alignment (first point):", points[0])

    aligned = align_to_vehicle_frame(points)
    print("After alignment (first point):", aligned[0])