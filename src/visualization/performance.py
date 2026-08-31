import time


def measure_pipeline_fps(pipeline_function, *args, **kwargs):
    """
    Measures how long one run of the pipeline takes, and calculates FPS.
    
    Args:
        pipeline_function: the function to run and time (e.g. run_pipeline)
        *args, **kwargs: arguments to pass to that function
    
    Returns:
        result: whatever the pipeline function returns
        elapsed_seconds: time taken in seconds
        fps: frames per second (1 / elapsed_seconds)
    """
    start_time = time.time()
    result = pipeline_function(*args, **kwargs)
    end_time = time.time()
    
    elapsed_seconds = end_time - start_time
    fps = 1.0 / elapsed_seconds if elapsed_seconds > 0 else 0.0
    
    return result, elapsed_seconds, fps


if __name__ == "__main__":
    from src.visualization.dashboard import run_pipeline

    grid, elapsed, fps = measure_pipeline_fps(run_pipeline, num_points=5000)

    print(f"Pipeline took: {elapsed:.4f} seconds")
    print(f"FPS: {fps:.2f}")
    print(f"Grid cells created: {grid.get_cell_count()}")