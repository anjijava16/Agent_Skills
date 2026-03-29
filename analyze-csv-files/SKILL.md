---
name: analyze-csv-files
description: >
  Analyze CSV files — load, inspect, clean, filter, aggregate, and summarize
  tabular data from CSV and TSV files. Use when the user has a CSV file and
  wants to understand its contents, find patterns, compute statistics, filter
  rows, or answer questions about the data, even if they just say "look at
  this spreadsheet" or "what's in this file."
license: MIT
compatibility: Requires Python 3.10+ and pip
metadata:
  author: welcome
  version: "1.0"
---

# Analyze CSV Files

## When to use this skill

Use this skill when the user needs to:
- Load and inspect a CSV or TSV file
- Get summary statistics (row count, column types, missing values)
- Filter, sort, or search rows by conditions
- Aggregate data (group by, sum, count, average)
- Find top/bottom N items by a column
- Answer specific questions about CSV data
- Clean CSV data (fix types, handle missing values, deduplicate)

## Prerequisites

```bash
pip install pandas tabulate
```

## Quick Inspection

Always start by inspecting the file before any analysis:

```python
import pandas as pd

df = pd.read_csv("data.csv")

print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")
print(f"Columns and types:\n{df.dtypes.to_string()}\n")
print(f"First 5 rows:\n{df.head().to_markdown(index=False)}\n")

missing = df.isnull().sum()
if missing.any():
    print(f"Missing values:\n{missing[missing > 0].to_string()}")
else:
    print("No missing values")
```

Run `scripts/inspect_csv.py` for a one-command overview.

## Filtering Rows

```python
# By condition
high_revenue = df[df["revenue"] > 10000]

# Multiple conditions
filtered = df[(df["status"] == "active") & (df["age"] >= 18)]

# String contains (case-insensitive)
matches = df[df["name"].str.contains("smith", case=False, na=False)]

# Date range
df["date"] = pd.to_datetime(df["date"])
recent = df[df["date"] >= "2025-01-01"]
```

## Sorting

```python
# Sort by one column (descending)
top = df.sort_values("revenue", ascending=False)

# Sort by multiple columns
sorted_df = df.sort_values(["category", "revenue"], ascending=[True, False])

# Top N
top_10 = df.nlargest(10, "revenue")
bottom_5 = df.nsmallest(5, "price")
```

## Aggregation

```python
# Group by and aggregate
summary = df.groupby("category").agg(
    count=("id", "count"),
    total=("revenue", "sum"),
    average=("revenue", "mean"),
).sort_values("total", ascending=False)

print(summary.to_markdown())
```

```python
# Pivot table
pivot = df.pivot_table(
    values="revenue",
    index="region",
    columns="quarter",
    aggfunc="sum",
    fill_value=0,
)
print(pivot.to_markdown())
```

## Summary Statistics

```python
# Full numeric summary
print(df.describe().to_markdown())

# Value counts for a categorical column
print(df["status"].value_counts().to_markdown())

# Unique values
print(f"Unique categories: {df['category'].nunique()}")
print(df["category"].unique())
```

## Cleaning

```python
# Remove duplicates
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicates")

# Handle missing values
df["numeric_col"] = df["numeric_col"].fillna(df["numeric_col"].median())
df["text_col"] = df["text_col"].fillna("Unknown")

# Fix currency strings → float
df["price"] = df["price"].str.replace(r"[$,]", "", regex=True).astype(float)

# Strip whitespace from string columns
for col in df.select_dtypes(include="object"):
    df[col] = df[col].str.strip()
```

## Saving Results

```python
# Save cleaned/filtered data
df.to_csv("output.csv", index=False)

# Save specific columns
df[["name", "email", "revenue"]].to_csv("subset.csv", index=False)

# Save as TSV
df.to_csv("output.tsv", sep="\t", index=False)
```

## Gotchas

- **Always inspect first**: Run `df.shape`, `df.dtypes`, `df.head()` before any analysis. Wrong assumptions about column types cause silent bugs.
- **Encoding issues**: If `read_csv` fails with UnicodeDecodeError, try `encoding="latin1"` or `encoding="utf-8-sig"` (for files with BOM).
- **CSV delimiter**: Not all "CSV" files use commas. Check for semicolons (`sep=";"`) or tabs (`sep="\t"`). Use `pd.read_csv("file.csv", sep=None, engine="python")` to auto-detect.
- **Header row**: Some files have no header. Use `header=None` and assign `df.columns = [...]`.
- **Numbers as strings**: Columns with `$`, `,`, or `%` load as strings. Strip formatting first, then convert to float.
- **Dates**: Always convert with `pd.to_datetime(col, errors="coerce")` so bad dates become `NaT` instead of crashing.
- **Index in output**: Always use `index=False` in `to_csv()` and `to_markdown()` unless the index is meaningful.

## Validation

After analysis:
1. Verify row counts — no unintended data loss from filters or dedup
2. Check computed values are within expected ranges
3. Ensure output CSV is readable: `pd.read_csv("output.csv").head()`
4. Never overwrite the original file — always save to a new filename

## References

- See [references/REFERENCE.md](references/REFERENCE.md) for advanced patterns (multi-file joins, window functions, large file handling)
