
import pandas as pd
from benchmark_utils import measure_execution


def sample_operation():
    df = pd.DataFrame({
        "close": [109.50, 110.00, 109.50, 109.10, 109.20]
    })

    return df["close"].mean()


result, elapsed, peak_memory = measure_execution(sample_operation)

print("===== BENCHMARK TEST =====")
print(f"Mean close: {result:.2f}")
print(f"Execution time: {elapsed:.6f} seconds")
print(f"Peak process memory: {peak_memory:.2f} MB")
