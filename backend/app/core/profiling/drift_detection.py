import polars as pl
import numpy as np
from scipy.stats import ks_2samp
from typing import Dict, Any


def detect_drift(df_reference: pl.DataFrame, df_current: pl.DataFrame) -> Dict[str, Any]:
    common_cols = set(df_reference.columns) & set(df_current.columns)
    results = {}

    for col in common_cols:
        if df_reference[col].dtype not in (pl.Float64, pl.Float32, pl.Int64, pl.Int32):
            continue

        ref = df_reference[col].drop_nulls().to_numpy()
        cur = df_current[col].drop_nulls().to_numpy()

        if len(ref) < 10 or len(cur) < 10:
            continue

        stat, p_value = ks_2samp(ref, cur)
        drift_detected = p_value < 0.05

        results[col] = {
            "ks_statistic": round(float(stat), 4),
            "p_value": round(float(p_value), 6),
            "drift_detected": drift_detected,
            "severity": "high" if p_value < 0.01 else "medium" if drift_detected else "none",
        }

    return results
