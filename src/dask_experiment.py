
from pathlib import Path
import dask
import dask.dataframe as dd
from benchmark_utils import measure_execution

FILE_PATH = Path("data/combined_over_5gb.csv")


def run_dask_experiment():
    # Build the Dask DataFrame (lazy evaluation)
    df = dd.read_csv(FILE_PATH, blocksize="128MB")

    # Define aggregations without loading the entire dataset
    row_count = df["close"].count()
    mean_close = df["close"].mean()

    # Compute both results together to optimize the task graph
    rows, mean_value = dask.compute(row_count, mean_close)

    return {
        "rows": int(rows),
        "mean_close": float(mean_value),
    }


if not FILE_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {FILE_PATH}")

print("===== DASK DATAFRAME EXPERIMENT =====")
print(f"File size: {FILE_PATH.stat().st_size / (1024 ** 3):.2f} GB")
print("Partition size: 128 MB")
print("Building the lazy computation graph...")

result, elapsed, peak_memory = measure_execution(run_dask_experiment)

print("\n===== DASK EXPERIMENT COMPLETED =====")
print(f"Total rows with non-missing close values: {result['rows']:,}")
print(f"Mean close: {result['mean_close']:.6f}")
print(f"Execution time: {elapsed:.2f} seconds")
print(f"Peak process memory: {peak_memory:.2f} MB")
