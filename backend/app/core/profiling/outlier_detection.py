import polars as pl
import numpy as np
from typing import Dict, Any


def detect_outliers(df: pl.DataFrame) -> Dict[str, Any]:
    result = {}
    numeric_cols = [col for col in df.columns if df[col].dtype in (pl.Float64, pl.Float32, pl.Int64, pl.Int32)]

    for col in numeric_cols:
        series = df[col].drop_nulls().to_numpy()
        if len(series) < 10:
            continue

        q1, q3 = np.percentile(series, 25), np.percentile(series, 75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outlier_mask = (series < lower) | (series > upper)
        outlier_count = int(outlier_mask.sum())

        result[col] = {
            "outlier_count": outlier_count,
            "outlier_pct": round((outlier_count / len(series)) * 100, 2),
            "lower_bound": round(float(lower), 4),
            "upper_bound": round(float(upper), 4),
            "method": "IQR",
        }
    return result
