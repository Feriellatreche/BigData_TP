
from pathlib import Path
import zipfile
import pandas as pd
from io import BytesIO

zip_path = Path(r"C:\Users\DELL\Downloads\archive (1).zip")
target = "China A shares 2000_2009/2009/2009/600519.SH.csv"

with zipfile.ZipFile(zip_path, "r") as z:
    with z.open(target) as f:
        sample = f.read(200_000)

df = pd.read_csv(BytesIO(sample), nrows=5)

print("===== CSV STRUCTURE =====")
print("Columns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.to_string(index=False))
