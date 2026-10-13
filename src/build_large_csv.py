
import zipfile
from pathlib import Path

# Original ZIP file
ZIP_PATH = Path(r"C:\Users\DELL\Downloads\archive (1).zip")

# Output CSV file
OUTPUT_PATH = Path("data") / "combined_over_5gb.csv"

# Stop after reaching approximately 5.2 GB
TARGET_SIZE = int(5.2 * 1024**3)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

if not ZIP_PATH.exists():
    raise FileNotFoundError(f"ZIP file not found: {ZIP_PATH}")

csv_files = []

with zipfile.ZipFile(ZIP_PATH, "r") as archive:
    csv_files = sorted(
        name for name in archive.namelist()
        if name.lower().endswith(".csv")
        and not name.endswith("/")
    )

    print(f"CSV files found: {len(csv_files)}")
    print("Creating a CSV larger than 5 GB...")
    print("This may take some time.")

    total_bytes = 0
    files_used = 0

    with open(OUTPUT_PATH, "wb") as output:
        for filename in csv_files:
            with archive.open(filename, "r") as source:
                first_line = source.readline()

                # Write the header only once
                if files_used == 0:
                    output.write(first_line)
                    total_bytes += len(first_line)

                # Skip headers in subsequent files
                for line in source:
                    if total_bytes >= TARGET_SIZE:
                        break

                    output.write(line)
                    total_bytes += len(line)

            files_used += 1

            if files_used % 100 == 0:
                print(
                    f"Files processed: {files_used} | "
                    f"Output size: {total_bytes / 1024**3:.2f} GB"
                )

            if total_bytes >= TARGET_SIZE:
                break

print("\n===== FILE CREATION SUMMARY =====")
print(f"Files used: {files_used}")
print(f"Output path: {OUTPUT_PATH.resolve()}")
print(f"Output size: {OUTPUT_PATH.stat().st_size / 1024**3:.2f} GB")
print("Finished.")
