# Analyze CSV Files — Advanced Reference

## Joining Multiple CSV Files

```python
import pandas as pd

orders = pd.read_csv("orders.csv")
customers = pd.read_csv("customers.csv")

# Inner join
merged = pd.merge(orders, customers, on="customer_id", how="inner")

# Left join (keep all orders)
merged = pd.merge(orders, customers, on="customer_id", how="left")

# Join on different column names
merged = pd.merge(orders, customers, left_on="cust_id", right_on="id")
```

## Concatenating CSV Files

```python
import glob

files = glob.glob("data/*.csv")
dfs = [pd.read_csv(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)
print(f"Combined: {len(combined)} rows from {len(files)} files")
```

## Window Functions

```python
# Rolling average
df = df.sort_values("date")
df["revenue_7d_avg"] = df["revenue"].rolling(window=7).mean()

# Cumulative sum
df["cumulative"] = df["revenue"].expanding().sum()

# Rank within groups
df["rank"] = df.groupby("category")["revenue"].rank(ascending=False)
```

## Handling Large Files (>100MB)

```python
# Read in chunks
chunks = pd.read_csv("huge.csv", chunksize=50000)
results = []
for chunk in chunks:
    filtered = chunk[chunk["status"] == "active"]
    results.append(filtered)
df = pd.concat(results, ignore_index=True)
```

```python
# Reduce memory with dtypes
df = pd.read_csv("huge.csv", dtype={
    "id": "int32",
    "category": "category",
    "value": "float32",
})
```

## Cross-Tabulation

```python
ct = pd.crosstab(df["region"], df["product"], margins=True)
print(ct.to_markdown())
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ParserError: Error tokenizing data` | Inconsistent columns | `error_bad_lines=False` or check file manually |
| `UnicodeDecodeError` | Non-UTF8 encoding | `encoding="latin1"` or `encoding="cp1252"` |
| All data in one column | Wrong delimiter | `sep=";"` or `sep="\t"` or `sep=None, engine="python"` |
| Numbers read as strings | Thousands separator or currency | Strip with `.str.replace()` then `.astype(float)` |
| `SettingWithCopyWarning` | Chained assignment | Use `df.loc[mask, "col"] = value` |
| Memory error | File too large | Use `chunksize` or `dtype` optimization |
