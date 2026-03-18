import polars as pl
from typing import List, Dict, Any


def run_rule_engine(df: pl.DataFrame) -> List[Dict[str, Any]]:
    insights = []

    # Rule 1: High null columns
    for col in df.columns:
        null_pct = df[col].null_count() / df.shape[0] * 100
        if null_pct > 30:
            insights.append({
                "rule": "high_nulls",
                "column": col,
                "message": f"Column '{col}' has {null_pct:.1f}% missing values. Consider imputation or removal.",
                "severity": "warning",
            })

    # Rule 2: Constant columns
    for col in df.columns:
        if df[col].n_unique() == 1:
            insights.append({
                "rule": "constant_column",
                "column": col,
                "message": f"Column '{col}' has only one unique value. It carries no information.",
                "severity": "info",
            })

    # Rule 3: High cardinality string columns
    for col in df.columns:
        if df[col].dtype in (pl.Utf8, pl.String):
            if df[col].n_unique() > 0.9 * df.shape[0]:
                insights.append({
                    "rule": "high_cardinality",
                    "column": col,
                    "message": f"Column '{col}' has very high cardinality ({df[col].n_unique()} unique values). Likely an ID or free-text field.",
                    "severity": "info",
                })

    # Rule 4: Imbalanced binary columns
    for col in df.columns:
        if df[col].n_unique() == 2:
            counts = df[col].value_counts()
            if counts.shape[0] == 2:
                ratio = counts["count"][0] / (counts["count"][1] + 1e-9)
                if ratio > 9 or ratio < 0.11:
                    insights.append({
                        "rule": "class_imbalance",
                        "column": col,
                        "message": f"Column '{col}' appears heavily imbalanced (ratio ~{ratio:.1f}:1).",
                        "severity": "warning",
                    })

    return insights
