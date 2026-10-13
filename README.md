# Big Data Processing: Pandas, Chunking, and Dask

## 1. Project Overview

This project evaluates different approaches to processing a large CSV dataset exceeding 5 GB. It compares Standard Pandas, Pandas Chunking, and Dask DataFrame in terms of execution time, memory consumption, and aggregation results.

The dataset contains stock market minute-bar records. The experiments calculate the number of rows with valid closing prices and the mean of the `close` column.

## 2. Dataset Description

- **Dataset type:** Stock market minute-bar data
- **CSV file:** `data/combined_over_5gb.csv`
- **File size:** Approximately 5.20 GB
- **Number of rows:** 98,777,445
- **Number of columns:** 7
- **Aggregation column:** `close`

The combined CSV file was created by concatenating multiple CSV files while retaining a single header.

The dataset is stored locally and is not included in the GitHub repository because of its large size.

## 3. Project Objectives

The main objectives are:

1. Attempt to load the entire CSV file using standard Pandas.
2. Process the dataset incrementally using Pandas Chunking.
3. Process the dataset using Dask DataFrame and partitioned computation.
4. Measure execution time and approximate peak process memory.
5. Compare aggregation results across the three approaches.
6. Analyze the trade-offs between execution speed and memory consumption.

## 4. Technologies Used

- Python 3.12
- Pandas
- Dask DataFrame
- PyArrow
- psutil
- Matplotlib

Pandas handles CSV processing and result storage. Dask supports partitioned computations and lazy evaluation. PyArrow provides supporting functionality for Dask, while psutil is used to measure process memory consumption.

## 5. Project Structure

```text
BigData_TP/
├── data/
│   └── combined_over_5gb.csv
├── src/
│   ├── benchmark_utils.py
│   ├── inspect_large_csv.py
│   ├── test_benchmark.py
│   ├── pandas_standard_experiment.py
│   ├── pandas_chunk_experiment.py
│   ├── compare_chunk_sizes.py
│   ├── dask_experiment.py
│   └── save_benchmark_results.py
├── results/
│   ├── benchmark_results.csv
│   └── chunk_size_comparison.csv
├── README.md
├── requirements.txt
└── .gitignore
```

This structure represents the expected organization. Keep only files that actually exist in the project.

## 6. Experimental Methodology

### 6.1 Standard Pandas

Standard Pandas loads the entire CSV file into memory using `pandas.read_csv()`.

The experiment measures:

- Number of rows
- Mean of the `close` column
- Execution time
- Approximate peak process memory

This method is straightforward but can require substantial memory when processing large datasets.

### 6.2 Pandas Chunking

Pandas Chunking processes the dataset in smaller portions using:

```python
pd.read_csv(FILE_PATH, chunksize=100_000)
```

For each chunk, the experiment accumulates the sum and count of valid `close` values. The final mean is calculated without retaining the complete dataset in memory.

\[
\text{Mean Close} =
\frac{\text{Sum of valid close values}}
{\text{Number of valid close values}}
\]

The project also compares chunk sizes of 10,000, 100,000, and 500,000 rows.

### 6.3 Dask DataFrame

Dask reads the CSV file in partitions of approximately 128 MB:

```python
df = dd.read_csv(FILE_PATH, blocksize="128MB")
```

Instead of immediately performing all operations, Dask builds a computation graph representing the requested calculations.

#### Lazy Evaluation

Lazy evaluation means that Dask can define operations before executing them. The calculations are triggered when the results are explicitly requested, such as through `dask.compute()`.

#### Compute Graph Optimization

The experiment defines the row count and mean as lazy expressions and computes them together:

```python
row_count = df["close"].count()
mean_close = df["close"].mean()

rows, mean_value = dask.compute(row_count, mean_close)
```

Submitting both calculations together allows Dask to coordinate the work through a shared computation graph and potentially reuse intermediate work. This avoids unnecessarily triggering separate computations for each result.

Dask processes the partitions without requiring the entire dataset to be loaded into one Pandas DataFrame.

## 7. Experimental Results

### 7.1 Standard Pandas

- **Status:** Success
- **Total rows:** 98,777,445
- **Mean closing price:** 15.388846
- **Execution time:** 112.95 seconds
- **Peak process memory:** 9735.02 MB

The experiment successfully loaded the entire dataset, but it consumed substantially more memory than the incremental approach.

### 7.2 Pandas Chunking

- **Status:** Success
- **Total rows:** 98,777,445
- **Mean closing price:** 15.388846
- **Execution time:** 91.87 seconds
- **Peak process memory:** 124.40 MB
- **Chunk size:** 100,000 rows

Chunking greatly reduced measured memory consumption by processing the dataset incrementally.

### 7.3 Dask DataFrame

- **Status:** Success
- **Rows with non-missing `close` values:** 98,777,445
- **Mean closing price:** 15.388846
- **Execution time:** 73.26 seconds
- **Peak process memory:** 3910.42 MB
- **Partition size:** Approximately 128 MB

Dask achieved the shortest execution time in the recorded experiments. Its measured memory consumption was higher than that of Pandas Chunking but lower than that of Standard Pandas.

## 8. Overall Comparison

| Method | Execution Time (s) | Peak Process Memory (MB) | Status |
|---|---:|---:|---|
| Standard Pandas | 112.95 | 9735.02 | Success |
| Pandas Chunking (100,000) | 91.87 | 124.40 | Success |
| Dask DataFrame | 73.26 | 3910.42 | Success |

All three approaches produced the same mean closing price: **15.388846**.

Dask was the fastest approach in these recorded runs. Pandas Chunking had the lowest measured process memory consumption. Standard Pandas had the highest memory consumption because it loaded the entire dataset into one DataFrame.

The memory values are approximate peak process measurements, not total system memory measurements. Results can vary depending on available resources, caching, and runtime conditions.

## 9. Chunk-Size Comparison

The chunk-size experiment compared three different values.

| Chunk Size (rows) | Total Rows | Mean Close | Execution Time (s) | Peak Process Memory (MB) |
|---:|---:|---:|---:|---:|
| 10,000 | 98,777,445 | 15.388846 | 161.03 | 94.90 |
| 100,000 | 98,777,445 | 15.388846 | 91.23 | 125.92 |
| 500,000 | 98,777,445 | 15.388846 | 77.85 | 193.64 |

In these runs, larger chunks reduced execution time but increased memory consumption. The appropriate chunk size depends on the available memory and performance requirements.

The values differ slightly from the separate 100,000-row experiment because execution conditions can vary between runs.

## 10. Saved Results

The following result files are available in the project:

- `results/benchmark_results.csv` — comparison of Standard Pandas, Pandas Chunking, and Dask.
- `results/chunk_size_comparison.csv` — comparison of different Pandas chunk sizes.

The script `src/benchmark_utils.py` provides the timing and approximate peak-memory measurement utility.

## 11. Installation and Execution

### Install dependencies

Activate the project's virtual environment and run:

```bash
python -m pip install -r requirements.txt
```

### Run the experiments

Execute commands from the project root directory:

```bash
python src/inspect_large_csv.py
python src/pandas_standard_experiment.py
python src/pandas_chunk_experiment.py
python src/compare_chunk_sizes.py
python src/dask_experiment.py
python src/save_benchmark_results.py
```

The dataset must exist at `data/combined_over_5gb.csv` before running the experiments.

**Important:** Standard Pandas may require substantial available memory. Do not run all experiments simultaneously. Re-running experiments may produce different timing and memory measurements.

## 12. Conclusion

This project demonstrates the trade-offs between conventional in-memory processing, incremental processing, and lazy partitioned computation.

Standard Pandas is simple to use but required the most memory in these experiments. Pandas Chunking achieved the lowest measured memory consumption by processing the dataset incrementally. Dask achieved the shortest execution time in the recorded runs and demonstrated how lazy evaluation and coordinated computation can support large-data processing.

All three approaches produced the same mean closing price, indicating consistent aggregation results across the experiments.
