import polars as pl
from typing import Dict, Any


def compute_dqi(df: pl.DataFrame, missing: Dict, outliers: Dict) -> Dict[str, Any]:
    """
    Data Quality Index (DQI) — scored 0 to 100.
    Weights: completeness 40%, uniqueness 20%, consistency 20%, outlier_ratio 20%
    """
    total_cells = df.shape[0] * df.shape[1]

    # Completeness
    total_missing = sum(v["missing_count"] for v in missing.values())
    completeness = 1 - (total_missing / total_cells) if total_cells > 0 else 1.0

    # Uniqueness (penalize near-duplicate rows)
    duplicate_ratio = df.is_duplicated().sum() / df.shape[0] if df.shape[0] > 0 else 0
    uniqueness = 1 - duplicate_ratio

    # Consistency (type mismatch proxy: count null-heavy columns)
    null_heavy = sum(1 for v in missing.values() if v["missing_pct"] > 50)
    consistency = 1 - (null_heavy / df.shape[1]) if df.shape[1] > 0 else 1.0

    # Outlier penalty
    total_outliers = sum(v.get("outlier_count", 0) for v in outliers.values())
    outlier_ratio = total_outliers / total_cells if total_cells > 0 else 0
    outlier_score = 1 - min(outlier_ratio, 1.0)

    score = round(
        (completeness * 0.4 + uniqueness * 0.2 + consistency * 0.2 + outlier_score * 0.2) * 100,
        2,
    )

    return {
        "score": score,
        "completeness": round(completeness * 100, 2),
        "uniqueness": round(uniqueness * 100, 2),
        "consistency": round(consistency * 100, 2),
        "outlier_score": round(outlier_score * 100, 2),
        "grade": _grade(score),
    }


def _grade(score: float) -> str:
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 40:
        return "D"
    return "F"
