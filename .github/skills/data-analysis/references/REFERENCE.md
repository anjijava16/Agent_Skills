# Data Analysis — Advanced Reference

## Pivot Tables

```python
pivot = df.pivot_table(
    values="revenue",
    index="region",
    columns="quarter",
    aggfunc="sum",
    fill_value=0,
    margins=True,
)
print(pivot.to_markdown())
```

## GroupBy with Multiple Aggregations

```python
summary = df.groupby("category").agg(
    count=("id", "count"),
    total_revenue=("revenue", "sum"),
    avg_revenue=("revenue", "mean"),
    median_revenue=("revenue", "median"),
    max_order=("revenue", "max"),
).sort_values("total_revenue", ascending=False)

print(summary.to_markdown())
```

## Window Functions (Rolling/Expanding)

```python
# 7-day rolling average
df = df.sort_values("date")
df["revenue_7d_avg"] = df["revenue"].rolling(window=7).mean()

# Cumulative sum
df["cumulative_revenue"] = df["revenue"].expanding().sum()

# Percent change
df["revenue_pct_change"] = df["revenue"].pct_change()
```

## Outlier Detection

### IQR Method

```python
def flag_outliers_iqr(series, factor=1.5):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    return (series < lower) | (series > upper)

df["is_outlier"] = flag_outliers_iqr(df["revenue"])
print(f"Outliers: {df['is_outlier'].sum()} / {len(df)}")
```

### Z-Score Method

```python
from scipy import stats

z_scores = stats.zscore(df["revenue"].dropna())
outliers = (z_scores.abs() > 3)
print(f"Outliers (|z| > 3): {outliers.sum()}")
```

## Resampling Time Series

```python
df = df.set_index("date")

# Monthly aggregation
monthly = df.resample("M").agg({
    "revenue": "sum",
    "orders": "count",
})

# Weekly with custom start day (Monday)
weekly = df.resample("W-MON").sum()
```

## Merging Datasets

```python
# Inner join (only matching rows)
merged = pd.merge(orders, customers, on="customer_id", how="inner")

# Left join (keep all orders, add customer info where available)
merged = pd.merge(orders, customers, on="customer_id", how="left")

# Join on different column names
merged = pd.merge(orders, products, left_on="product_id", right_on="id")
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| All values are NaN after merge | Join key mismatch (type or case) | Check dtypes and whitespace: `df["key"].str.strip()` |
| `SettingWithCopyWarning` | Chained assignment | Use `.loc[]`: `df.loc[mask, "col"] = value` |
| `OutOfMemoryError` | Dataset too large | Use `dtype` param, `chunksize`, or switch to polars |
| Chart is empty | No matching data after filter | Check filter results: `len(df[mask])` |
| Wrong date sorting | Dates parsed as strings | Convert first: `pd.to_datetime()` |
