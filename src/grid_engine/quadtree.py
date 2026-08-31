import numpy as np


class GridCell:
    """
    Represents one cell in our variable-resolution grid.
    Stores the label (drivable/static_obstacle/dynamic_object) and height
    of whatever point(s) landed in this cell.
    """
    def __init__(self, cell_x, cell_y, cell_size):
        self.cell_x = cell_x          # cell's grid column index
        self.cell_y = cell_y          # cell's grid row index
        self.cell_size = cell_size    # size of this cell in meters
        self.label = None             # most important label seen in this cell
        self.height = None            # height (z) value stored for this cell
        self.point_count = 0          # how many points landed in this cell

    def update(self, label, height):
        """
        Updates this cell with a new point's data.
        If multiple points land in the same cell, we keep the highest-priority label
        (obstacles matter more than drivable ground) and the max height seen.
        """
        priority = {"dynamic_object": 3, "static_obstacle": 2, "non_drivable": 1, "drivable": 0}
        
        if self.label is None or priority.get(label, 0) > priority.get(self.label, 0):
            self.label = label
        
        if self.height is None or height > self.height:
            self.height = height
        
        self.point_count += 1


class VariableResolutionGrid:
    """
    The core adaptive grid engine.
    Instead of one uniform grid, this uses a dictionary of cells where each
    cell's size depends on its distance from the sensor (vehicle-centric).
    
    Using a dictionary keyed by (zone_index, cell_x, cell_y) avoids needing
    a true nested quadtree structure while still achieving variable resolution
    without alignment errors - each zone has its own independent, consistent grid.
    """
    def __init__(self, resolution_zones):
        self.resolution_zones = resolution_zones  # list of (max_radius, cell_size)
        self.cells = {}  # key: (zone_index, cell_x, cell_y) -> GridCell

    def _get_zone_and_cell_size(self, distance):
        for zone_index, (max_radius, cell_size) in enumerate(self.resolution_zones):
            if distance <= max_radius:
                return zone_index, cell_size
        return None, None

    def add_point(self, x, y, z, label):
        """
        Adds one labeled 3D point into the grid.
        Automatically determines which zone/cell size to use based on distance,
        then places the point into the correct cell (creating it if needed).
        """
        if not np.isfinite(x) or not np.isfinite(y) or not np.isfinite(z):
         return
        distance = np.sqrt(x**2 + y**2)
        zone_index, cell_size = self._get_zone_and_cell_size(distance)
        
        if zone_index is None:
            return  # point is beyond max range, ignore it
        
        cell_x = int(np.floor(x / cell_size))
        cell_y = int(np.floor(y / cell_size))
        key = (zone_index, cell_x, cell_y)
        
        if key not in self.cells:
            self.cells[key] = GridCell(cell_x, cell_y, cell_size)
        
        self.cells[key].update(label, z)

    def get_cell_count(self):
        return len(self.cells)

    def get_memory_estimate_bytes(self):
        """
        Rough memory estimate: each cell stores a handful of small values.
        This is a simplified estimate for comparison purposes.
        """
        bytes_per_cell = 64  # rough estimate: label ref + height + counts + overhead
        return len(self.cells) * bytes_per_cell


if __name__ == "__main__":
    from src.grid_engine.resolution_config import RESOLUTION_ZONES

    grid = VariableResolutionGrid(RESOLUTION_ZONES)

    # Add a few test points manually
    grid.add_point(x=3.0, y=2.0, z=0.05, label="drivable")
    grid.add_point(x=3.05, y=2.02, z=0.05, label="drivable")  # same cell as above
    grid.add_point(x=15.0, y=10.0, z=1.5, label="static_obstacle")
    grid.add_point(x=60.0, y=30.0, z=0.8, label="dynamic_object")
    grid.add_point(x=200.0, y=100.0, z=0.0, label="drivable")  # out of range, ignored

    print(f"Total cells created: {grid.get_cell_count()}")
    print(f"Estimated memory: {grid.get_memory_estimate_bytes()} bytes")
    
    for key, cell in grid.cells.items():
        print(f"Zone {key[0]}, cell ({key[1]},{key[2]}) -> label: {cell.label}, height: {cell.height}, points: {cell.point_count}")