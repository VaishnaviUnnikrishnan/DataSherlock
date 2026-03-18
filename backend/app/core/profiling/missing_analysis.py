import polars as pl
from typing import Dict, Any


def analyze_missing(df: pl.DataFrame) -> Dict[str, Any]:
    result = {}
    for col in df.columns:
        missing_count = df[col].null_count()
        missing_pct = round((missing_count / df.shape[0]) * 100, 2) if df.shape[0] > 0 else 0
        result[col] = {
            "missing_count": missing_count,
            "missing_pct": missing_pct,
            "severity": _severity(missing_pct),
        }
    return result


def _severity(pct: float) -> str:
    if pct == 0:
        return "none"
    elif pct <= 5:
        return "low"
    elif pct <= 20:
        return "medium"
    elif pct <= 50:
        return "high"
    return "critical"
