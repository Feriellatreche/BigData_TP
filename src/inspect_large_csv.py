
from pathlib import Path
import pandas as pd

file_path = Path("data/combined_over_5gb.csv")

print("===== LARGE CSV INSPECTION =====")
print(f"File exists: {file_path.exists()}")

if not file_path.exists():
    raise FileNotFoundError(file_path)

size_gb = file_path.stat().st_size / (1024 ** 3)
print(f"File size: {size_gb:.2f} GB")

# Read only the header and first 5 rows
sample = pd.read_csv(file_path, nrows=5)

print("\nColumns:")
print(sample.columns.tolist())

print("\nFirst 5 rows:")
print(sample)

print("\nData types:")
print(sample.dtypes)

print("\nInspection completed successfully.")
