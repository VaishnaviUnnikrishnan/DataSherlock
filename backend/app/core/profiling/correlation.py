import polars as pl
import numpy as np
from typing import Dict, Any


def compute_correlation(df: pl.DataFrame) -> Dict[str, Any]:
    numeric_cols = [
        col for col in df.columns
        if df[col].dtype in (pl.Float64, pl.Float32, pl.Int64, pl.Int32)
    ]

    if len(numeric_cols) < 2:
        return {"matrix": {}, "strong_pairs": []}

    sub = df.select(numeric_cols).drop_nulls()
    arr = sub.to_numpy()
    corr_matrix = np.corrcoef(arr.T)

    matrix = {}
    strong_pairs = []

    for i, ci in enumerate(numeric_cols):
        matrix[ci] = {}
        for j, cj in enumerate(numeric_cols):
            val = round(float(corr_matrix[i, j]), 4)
            matrix[ci][cj] = val
            if i < j and abs(val) >= 0.7:
                strong_pairs.append({"col_a": ci, "col_b": cj, "correlation": val})

    return {"matrix": matrix, "strong_pairs": strong_pairs}
