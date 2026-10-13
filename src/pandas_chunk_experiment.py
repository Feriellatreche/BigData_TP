
from pathlib import Path
import pandas as pd
from benchmark_utils import measure_execution

FILE_PATH = Path("data/combined_over_5gb.csv")
CHUNK_SIZE = 100_000


def read_csv_in_chunks():
    total_rows = 0
    total_chunks = 0
    close_sum = 0.0
    close_count = 0

    for chunk in pd.read_csv(FILE_PATH, chunksize=CHUNK_SIZE):
        total_rows += len(chunk)
        total_chunks += 1

        if "close" in chunk.columns:
            close_sum += chunk["close"].sum()
            close_count += chunk["close"].count()

    mean_close = (
        close_sum / close_count
        if close_count > 0
        else float("nan")
    )

    return {
        "total_rows": total_rows,
        "total_chunks": total_chunks,
        "mean_close": mean_close,
    }


if not FILE_PATH.exists():
    raise FileNotFoundError(FILE_PATH)

result, elapsed, peak_memory = measure_execution(
    read_csv_in_chunks
)

print("===== PANDAS CHUNK EXPERIMENT =====")
print(f"File size: {FILE_PATH.stat().st_size / 1024**3:.2f} GB")
print(f"Chunk size: {CHUNK_SIZE:,} rows")
print(f"Total rows: {result['total_rows']:,}")
print(f"Total chunks: {result['total_chunks']:,}")
print(f"Mean close: {result['mean_close']:.4f}")
print(f"Execution time: {elapsed:.4f} seconds")
print(f"Peak process memory: {peak_memory:.2f} MB")
