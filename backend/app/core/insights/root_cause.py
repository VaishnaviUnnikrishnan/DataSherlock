import polars as pl
from typing import List, Dict, Any


def analyze_root_cause(df: pl.DataFrame) -> List[Dict[str, Any]]:
    """
    Heuristic root-cause analysis based on column patterns and statistical properties.
    """
    findings = []

    numeric_cols = [
        col for col in df.columns
        if df[col].dtype in (pl.Float64, pl.Float32, pl.Int64, pl.Int32)
    ]

    for col in numeric_cols:
        series = df[col].drop_nulls()
        if series.is_empty():
            continue

        mean = series.mean()
        std = series.std()
        skew = series.skew()

        if skew is not None and abs(skew) > 2:
            findings.append({
                "column": col,
                "finding": "high_skewness",
                "description": f"'{col}' is heavily skewed (skew={skew:.2f}). Consider log or box-cox transformation.",
                "suggested_action": "apply_log_transform",
            })

        if std is not None and mean is not None and mean != 0:
            cv = std / abs(mean)
            if cv > 1:
                findings.append({
                    "column": col,
                    "finding": "high_variance",
                    "description": f"'{col}' has high coefficient of variation ({cv:.2f}). Data may be heterogeneous.",
                    "suggested_action": "investigate_subgroups",
                })

    return findings
