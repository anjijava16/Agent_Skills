---
name: data-analysis
description: >
  Analyze datasets — compute summary statistics, clean messy data, add derived
  columns, detect outliers, and generate charts. Use when the user has a CSV,
  TSV, Excel, or JSON data file and wants to explore, transform, visualize, or
  understand the data, even if they don't explicitly mention "analysis."
license: MIT
compatibility: Requires Python 3.10+ and pip
metadata:
  author: welcome
  version: "1.0"
---

# Data Analysis

## When to use this skill

Use this skill when the user needs to:
- Load and explore a dataset (CSV, TSV, Excel, JSON, Parquet)
- Compute summary statistics (mean, median, distribution, correlations)
- Clean data (handle missing values, fix types, remove duplicates)
- Add derived columns or transform existing ones
- Detect outliers or anomalies
- Generate charts and visualizations
- Answer questions about data ("what's the trend?", "which month was highest?")

## Prerequisites

```bash
pip install pandas matplotlib seaborn openpyxl
```

For larger datasets or advanced analysis:

```bash
pip install scipy scikit-learn plotly
```

## Loading Data

Use pandas. Auto-detect the format from the file extension.

```python
import pandas as pd

# CSV (most common)
df = pd.read_csv("data.csv")

# Excel
df = pd.read_excel("data.xlsx", sheet_name=0)

# TSV
df = pd.read_csv("data.tsv", sep="\t")

# JSON (records-oriented)
df = pd.read_json("data.json")

# Parquet
df = pd.read_parquet("data.parquet")
```

**First step after loading**: Always inspect the data before doing anything else.

```python
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\nColumns:\n{df.dtypes.to_string()}")
print(f"\nFirst 5 rows:\n{df.head().to_markdown(index=False)}")
print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0].to_string()}")
```

## Summary Statistics

```python
# Numeric columns
print(df.describe().to_markdown())

# Categorical columns
for col in df.select_dtypes(include="object").columns:
    print(f"\n{col}: {df[col].nunique()} unique values")
    print(df[col].value_counts().head(10).to_string())
```

### Correlations

```python
corr = df.select_dtypes(include="number").corr()
print(corr.to_markdown())

# Heatmap
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=150)
plt.close()
```

## Data Cleaning

### Handle Missing Values

```python
# Check what's missing
print(df.isnull().sum()[df.isnull().sum() > 0])

# Drop rows where key columns are missing
df = df.dropna(subset=["important_column"])

# Fill numeric columns with median (robust to outliers)
for col in df.select_dtypes(include="number").columns:
    df[col] = df[col].fillna(df[col].median())

# Fill categorical with mode
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].fillna(df[col].mode()[0])
```

### Fix Data Types

```python
# Dates stored as strings
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Numbers stored as strings (e.g., "$1,234.56")
df["price"] = df["price"].str.replace(r"[$,]", "", regex=True).astype(float)

# Categories
df["status"] = df["status"].astype("category")
```

### Remove Duplicates

```python
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicate rows")

# Or deduplicate on specific columns
df = df.drop_duplicates(subset=["id"], keep="last")
```

## Derived Columns

```python
# Arithmetic
df["profit_margin"] = (df["revenue"] - df["cost"]) / df["revenue"] * 100

# Time-based
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day_of_week"] = df["date"].dt.day_name()

# Binning
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 35, 55, 100],
                          labels=["<18", "18-35", "36-55", "55+"])

# Conditional
df["status"] = df["score"].apply(lambda x: "pass" if x >= 70 else "fail")
```

## Visualization

Use matplotlib + seaborn. Always include titles and axis labels.

### Bar Chart

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
top = df.groupby("category")["revenue"].sum().sort_values(ascending=False).head(10)
sns.barplot(x=top.values, y=top.index, palette="viridis")
plt.xlabel("Total Revenue ($)")
plt.ylabel("Category")
plt.title("Top 10 Categories by Revenue")
plt.tight_layout()
plt.savefig("bar_chart.png", dpi=150)
plt.close()
```

### Line Chart (Time Series)

```python
plt.figure(figsize=(12, 6))
monthly = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum()
monthly.plot(kind="line", marker="o")
plt.xlabel("Month")
plt.ylabel("Revenue ($)")
plt.title("Monthly Revenue Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("line_chart.png", dpi=150)
plt.close()
```

### Histogram

```python
plt.figure(figsize=(8, 5))
df["price"].hist(bins=30, edgecolor="black")
plt.xlabel("Price ($)")
plt.ylabel("Frequency")
plt.title("Price Distribution")
plt.tight_layout()
plt.savefig("histogram.png", dpi=150)
plt.close()
```

### Scatter Plot

```python
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="feature_a", y="feature_b", hue="category", alpha=0.7)
plt.title("Feature A vs Feature B")
plt.tight_layout()
plt.savefig("scatter.png", dpi=150)
plt.close()
```

## Gotchas

- **Always inspect before analyzing**: Run `df.shape`, `df.dtypes`, `df.head()`, and `df.isnull().sum()` before any analysis. Wrong assumptions about data types or missing values cause subtle bugs.
- **Use `plt.close()` after every chart**: Without it, figures accumulate in memory. Always `savefig()` then `close()`.
- **Currency/number strings**: Columns like `"$1,234.56"` load as strings. Strip formatting characters before converting to float.
- **Date parsing**: Always use `errors="coerce"` with `pd.to_datetime()` so bad dates become `NaT` instead of crashing.
- **Excel sheet names**: `read_excel()` loads the first sheet by default. Check `pd.ExcelFile("file.xlsx").sheet_names` first.
- **Large files (>100MB)**: Use `dtype` parameter to reduce memory, or load with `chunksize` for streaming.
- **Index in output**: Use `index=False` in `to_csv()`, `to_markdown()`, and `to_excel()` unless the index is meaningful.

## Validation

After analysis:
1. Verify row counts match expectations (no unintended drops)
2. Check that computed values are within reasonable ranges
3. For charts, confirm axes are labeled and data is correctly represented
4. Save cleaned data as a new file — never overwrite the original

## References

- See [references/REFERENCE.md](references/REFERENCE.md) for advanced patterns (pivot tables, groupby, window functions, outlier detection)
