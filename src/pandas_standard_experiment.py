
from pathlib import Path
import time
import pandas as pd
import psutil
from benchmark_utils import measure_execution

FILE_PATH = Path("data/combined_over_5gb.csv")


def read_full_csv():
    df = pd.read_csv(FILE_PATH)

    return {
        "rows": len(df),
        "mean_close": df["close"].mean(),
        "columns": len(df.columns),
    }


if not FILE_PATH.exists():
    raise FileNotFoundError(FILE_PATH)

process = psutil.Process()
initial_memory = process.memory_info().rss / (1024 ** 2)

print("===== STANDARD PANDAS EXPERIMENT =====")
print(f"File size: {FILE_PATH.stat().st_size / (1024 ** 3):.2f} GB")
print(f"Initial process memory: {initial_memory:.2f} MB")
print("Attempting to load the entire CSV into memory...")
print("Monitor overall RAM usage in Windows Task Manager.")
print("Press Ctrl+C if the computer becomes unresponsive.")

try:
    result, elapsed, peak_memory = measure_execution(read_full_csv)

    print("\n===== EXPERIMENT SUCCEEDED =====")
    print(f"Total rows: {result['rows']:,}")
    print(f"Number of columns: {result['columns']}")
    print(f"Mean close: {result['mean_close']:.6f}")
    print(f"Execution time: {elapsed:.2f} seconds")
    print(f"Peak process memory: {peak_memory:.2f} MB")

except MemoryError:
    print("\n===== MEMORY ERROR =====")
    print("Pandas could not allocate the required memory.")

except KeyboardInterrupt:
    print("\n===== EXPERIMENT INTERRUPTED =====")
    print("The experiment was manually stopped.")

except Exception as exc:
    print("\n===== EXPERIMENT FAILED =====")
    print(f"Error type: {type(exc).__name__}")
    print(f"Error message: {exc}")
