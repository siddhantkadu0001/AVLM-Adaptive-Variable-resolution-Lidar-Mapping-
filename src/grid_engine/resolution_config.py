# Configuration for the adaptive variable-resolution grid.
# Defines zones by distance from the sensor, and the cell size used in each zone.

# Each zone: (max_radius_meters, cell_size_meters)
# Points are matched to the FIRST zone whose max_radius they fall within.
RESOLUTION_ZONES = [
    (10.0, 0.05),   # 0-10m radius  -> 5cm cells  (high detail, close range)
    (40.0, 0.20),   # 10-40m radius -> 20cm cells (medium detail)
    (100.0, 0.50),  # 40-100m radius -> 50cm cells (low detail, far range)
]


def get_cell_size(distance):
    """
    Given a point's distance from the sensor, returns the appropriate
    grid cell size for that distance, based on RESOLUTION_ZONES.
    
    Args:
        distance: distance from sensor in meters
    
    Returns:
        cell_size: size of grid cell (in meters) to use for this distance
                    Returns None if distance exceeds all defined zones.
    """
    for max_radius, cell_size in RESOLUTION_ZONES:
        if distance <= max_radius:
            return cell_size
    return None  # beyond max range, point is ignored


if __name__ == "__main__":
    test_distances = [3.0, 8.0, 15.0, 35.0, 60.0, 90.0, 150.0]
    for d in test_distances:
        cell_size = get_cell_size(d)
        print(f"Distance {d}m -> cell size: {cell_size}")