import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from src.preprocessing.loader import generate_fake_point_cloud
from src.preprocessing.filters import remove_outliers
from src.preprocessing.alignment import align_to_vehicle_frame
from src.terrain_analysis.model import classify_terrain
from src.object_detection.model import classify_objects
from src.fusion.label_fusion import fuse_labels
from src.grid_engine.projector import project_points_to_grid
from src.grid_engine.resolution_config import RESOLUTION_ZONES
from src.visualization.performance import measure_pipeline_fps


LABEL_COLORS = {
    "drivable": "#2ECC71",        # green
    "non_drivable": "#95A5A6",    # gray
    "static_obstacle": "#E74C3C", # red
    "dynamic_object": "#3498DB",  # blue
}


def run_pipeline(num_points):
    points = generate_fake_point_cloud(num_points=num_points)
    points = remove_outliers(points, max_distance=90.0)
    points = align_to_vehicle_frame(points)

    terrain_labels = classify_terrain(points)
    object_labels = classify_objects(points, terrain_labels)
    final_labels = fuse_labels(terrain_labels, object_labels)

    grid = project_points_to_grid(points, final_labels)
    return grid


def plot_grid(grid):
    fig, ax = plt.subplots(figsize=(8, 8))

    for (zone_index, cell_x, cell_y), cell in grid.cells.items():
        color = LABEL_COLORS.get(cell.label, "#000000")
        x = cell_x * cell.cell_size
        y = cell_y * cell.cell_size
        rect = plt.Rectangle((x, y), cell.cell_size, cell.cell_size, color=color)
        ax.add_patch(rect)

    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_aspect('equal')
    ax.set_facecolor('#1a1a1a')
    fig.patch.set_facecolor('#1a1a1a')
    ax.set_title("AVLM - 2.5D Variable Resolution Grid", color='white')
    ax.tick_params(colors='white')

    return fig


st.set_page_config(page_title="AVLM Dashboard", layout="wide")
st.title("AVLM: Adaptive Variable-Resolution Lidar Mapping")

num_points = st.sidebar.slider("Number of fake points", 500, 10000, 5000, step=500)

if st.sidebar.button("Run Pipeline"):
    grid, elapsed, fps = measure_pipeline_fps(run_pipeline, num_points)

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = plot_grid(grid)
        st.pyplot(fig)

    with col2:
        st.subheader("Performance Metrics")
        st.metric("Input Points", num_points)
        st.metric("Grid Cells Created", grid.get_cell_count())
        st.metric("Estimated Memory (bytes)", grid.get_memory_estimate_bytes())
        st.metric("Processing Time (s)", f"{elapsed:.4f}")
        st.metric("FPS", f"{fps:.2f}")

        naive_memory = num_points * 64
        savings = (1 - grid.get_memory_estimate_bytes() / naive_memory) * 100 if naive_memory > 0 else 0
        st.metric("Memory Savings vs Naive", f"{savings:.1f}%")

        st.subheader("Legend")
        for label, color in LABEL_COLORS.items():
            st.markdown(f"<span style='color:{color}'>■</span> {label}", unsafe_allow_html=True)
else:
    st.info("Click 'Run Pipeline' in the sidebar to generate a map.")