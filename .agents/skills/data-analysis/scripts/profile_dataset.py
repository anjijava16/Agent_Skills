#!/usr/bin/env python3
"""Quick dataset profiling: shape, types, missing values, basic stats."""

import sys

def profile(path: str) -> None:
    import pandas as pd

    ext = path.rsplit(".", 1)[-1].lower()
    loaders = {
        "csv": pd.read_csv,
        "tsv": lambda p: pd.read_csv(p, sep="\t"),
        "xlsx": pd.read_excel,
        "xls": pd.read_excel,
        "json": pd.read_json,
        "parquet": pd.read_parquet,
    }

    loader = loaders.get(ext)
    if not loader:
        print(f"Error: Unsupported format '.{ext}'. Supported: {', '.join(loaders)}", file=sys.stderr)
        sys.exit(1)

    df = loader(path)

    print(f"File: {path}")
    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")

    print("Columns:")
    for col in df.columns:
        missing = df[col].isnull().sum()
        missing_pct = f" ({missing / len(df) * 100:.1f}% missing)" if missing else ""
        print(f"  {col}: {df[col].dtype}{missing_pct}")

    print(f"\nFirst 5 rows:\n{df.head().to_markdown(index=False)}")

    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        print(f"\nNumeric summary:\n{numeric.describe().to_markdown()}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python profile_dataset.py <data_file>", file=sys.stderr)
        sys.exit(1)
    profile(sys.argv[1])
