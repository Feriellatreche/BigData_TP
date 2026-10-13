
from pathlib import Path
import pandas as pd
from benchmark_utils import measure_execution

FILE_PATH = Path("data/combined_over_5gb.csv")
CHUNK_SIZES = [10_000, 100_000, 500_000]


def read_with_chunk_size(chunk_size):
    def operation():
        total_rows = 0
        close_sum = 0.0
        close_count = 0

        for chunk in pd.read_csv(FILE_PATH, chunksize=chunk_size):
            total_rows += len(chunk)

            if "close" in chunk.columns:
                close_sum += chunk["close"].sum()
                close_count += chunk["close"].count()

        mean_close = (
            close_sum / close_count
            if close_count > 0
            else float("nan")
        )

        return total_rows, mean_close

    result, elapsed, peak_memory = measure_execution(operation)

    return {
        "chunk_size": chunk_size,
        "total_rows": result[0],
        "mean_close": result[1],
        "time_seconds": elapsed,
        "peak_memory_mb": peak_memory,
    }


if not FILE_PATH.exists():
    raise FileNotFoundError(FILE_PATH)

results = []

for size in CHUNK_SIZES:
    print(f"\nTesting chunk size: {size:,} rows")

    result = read_with_chunk_size(size)
    results.append(result)

    print(f"Rows: {result['total_rows']:,}")
    print(f"Mean close: {result['mean_close']:.4f}")
    print(f"Time: {result['time_seconds']:.4f} seconds")
    print(f"Peak process memory: {result['peak_memory_mb']:.2f} MB")

df_results = pd.DataFrame(results)

print("\n===== CHUNK SIZE COMPARISON =====")
print(df_results.to_string(index=False))

output_path = Path("results/chunk_size_comparison.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)
df_results.to_csv(output_path, index=False)

print(f"\nResults saved to: {output_path}")
