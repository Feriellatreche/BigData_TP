
from pathlib import Path
import pandas as pd

OUTPUT_PATH = Path("results/benchmark_results.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

results = [
    {
        "method": "Standard Pandas",
        "total_rows": 98777445,
        "mean_close": 15.388846,
        "execution_time_seconds": 112.95,
        "peak_process_memory_mb": 9735.02,
        "status": "Success",
    },
    {
        "method": "Pandas Chunking (100000)",
        "total_rows": 98777445,
        "mean_close": 15.388846,
        "execution_time_seconds": 91.8663,
        "peak_process_memory_mb": 124.40,
        "status": "Success",
    },
    {
        "method": "Dask DataFrame",
        "total_rows": 98777445,
        "mean_close": 15.388846,
        "execution_time_seconds": 73.26,
        "peak_process_memory_mb": 3910.42,
        "status": "Success",
    },
]

df = pd.DataFrame(results)
df.to_csv(OUTPUT_PATH, index=False)

print("Benchmark results saved successfully.")
print(f"File: {OUTPUT_PATH}")
print(df.to_string(index=False))
