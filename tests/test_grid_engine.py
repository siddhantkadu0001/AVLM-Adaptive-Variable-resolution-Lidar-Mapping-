import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from src.grid_engine.quadtree import VariableResolutionGrid
from src.grid_engine.resolution_config import RESOLUTION_ZONES, get_cell_size


def test_get_cell_size_close_range():
    """Test GE-01: Point within 10m gets small cell"""
    assert get_cell_size(5.0) == 0.05
    print("PASS: test_get_cell_size_close_range")


def test_get_cell_size_far_range():
    """Test GE-02: Point beyond 40m gets large cell"""
    assert get_cell_size(60.0) == 0.5
    print("PASS: test_get_cell_size_far_range")


def test_no_data_loss():
    """Test GE-03: No data loss during projection"""
    grid = VariableResolutionGrid(RESOLUTION_ZONES)
    num_points = 100
    
    for i in range(num_points):
        x = np.random.uniform(-50, 50)
        y = np.random.uniform(-50, 50)
        z = 0.0
        grid.add_point(x, y, z, "drivable")
    
    total_points_in_grid = sum(cell.point_count for cell in grid.cells.values())
    assert total_points_in_grid == num_points
    print("PASS: test_no_data_loss")


def test_out_of_range_point_dropped():
    """Test: point beyond 100m should be safely ignored, not crash"""
    grid = VariableResolutionGrid(RESOLUTION_ZONES)
    grid.add_point(x=500.0, y=500.0, z=0.0, label="drivable")
    assert grid.get_cell_count() == 0
    print("PASS: test_out_of_range_point_dropped")


def test_invalid_point_handled():
    """Test: NaN/infinity coordinates should be skipped, not crash"""
    grid = VariableResolutionGrid(RESOLUTION_ZONES)
    grid.add_point(x=float('nan'), y=5.0, z=0.0, label="drivable")
    assert grid.get_cell_count() == 0
    print("PASS: test_invalid_point_handled")


if __name__ == "__main__":
    test_get_cell_size_close_range()
    test_get_cell_size_far_range()
    test_no_data_loss()
    test_out_of_range_point_dropped()
    test_invalid_point_handled()
    print("\nAll tests passed!")