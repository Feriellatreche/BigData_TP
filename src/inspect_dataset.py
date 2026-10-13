
from pathlib import Path
import zipfile
import pandas as pd
from io import BytesIO

zip_path = Path(r"C:\Users\DELL\Downloads\archive (1).zip")

with zipfile.ZipFile(zip_path, "r") as z:
    csv_files = [
        name for name in z.namelist()
        if name.lower().endswith(".csv")
    ]

    reference_columns = None
    mismatches = []

    for name in csv_files[:100]:
        with z.open(name) as f:
            sample = f.read(100_000)

        df = pd.read_csv(BytesIO(sample), nrows=0)
        columns = df.columns.tolist()

        if reference_columns is None:
            reference_columns = columns
        elif columns != reference_columns:
            mismatches.append((name, columns))

print("Reference columns:", reference_columns)
print("Files checked:", min(100, len(csv_files)))
print("Files with different columns:", len(mismatches))

for name, columns in mismatches[:5]:
    print(name, columns)
