
import os
import time
import threading
import psutil


def measure_execution(func, sample_interval=0.05):
    """
    Measure execution time and approximate peak process memory.
    Returns: result, elapsed_seconds, peak_memory_mb
    """
    process = psutil.Process(os.getpid())
    peak_memory = process.memory_info().rss
    stop_monitoring = threading.Event()

    def monitor_memory():
        nonlocal peak_memory

        while not stop_monitoring.is_set():
            try:
                current_memory = process.memory_info().rss
                peak_memory = max(peak_memory, current_memory)
            except psutil.Error:
                pass

            stop_monitoring.wait(sample_interval)

    monitor = threading.Thread(target=monitor_memory, daemon=True)
    monitor.start()

    start_time = time.perf_counter()

    try:
        result = func()
    finally:
        elapsed = time.perf_counter() - start_time
        stop_monitoring.set()
        monitor.join()
        peak_memory = max(peak_memory, process.memory_info().rss)

    return result, elapsed, peak_memory / (1024 ** 2)
