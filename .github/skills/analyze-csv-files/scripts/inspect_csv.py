#!/usr/bin/env python3
"""Quick CSV inspection: shape, types, missing values, first rows, basic stats."""

import sys


def inspect_csv(path: str) -> None:
    import pandas as pd

    sep = "\t" if path.endswith(".tsv") else ","
    try:
        df = pd.read_csv(path, sep=sep)
    except UnicodeDecodeError:
        df = pd.read_csv(path, sep=sep, encoding="latin1")

    print(f"File: {path}")
    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")

    print("Columns:")
    for col in df.columns:
        missing = df[col].isnull().sum()
        missing_str = f" ({missing} missing, {missing/len(df)*100:.1f}%)" if missing else ""
        print(f"  {col}: {df[col].dtype}{missing_str}")

    print(f"\nFirst 5 rows:\n{df.head().to_markdown(index=False)}")

    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        print(f"\nNumeric summary:\n{numeric.describe().to_markdown()}")

    for col in df.select_dtypes(include="object").columns:
        n = df[col].nunique()
        if n <= 20:
            print(f"\n{col} value counts ({n} unique):")
            print(df[col].value_counts().head(10).to_string())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_csv.py <csv_file>", file=sys.stderr)
        sys.exit(1)
    inspect_csv(sys.argv[1])
