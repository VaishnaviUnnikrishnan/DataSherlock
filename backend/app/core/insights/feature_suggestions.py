import polars as pl
from typing import List, Dict, Any


def suggest_features(df: pl.DataFrame) -> List[Dict[str, Any]]:
    suggestions = []

    for col in df.columns:
        col_lower = col.lower()

        # Datetime decomposition
        if any(k in col_lower for k in ["date", "time", "timestamp"]):
            suggestions.append({
                "source_column": col,
                "suggestion": "datetime_decomposition",
                "description": f"Extract year, month, day, weekday, hour from '{col}'.",
                "new_features": [f"{col}_year", f"{col}_month", f"{col}_day", f"{col}_weekday"],
            })

        # Text length feature
        if df[col].dtype in (pl.Utf8, pl.String):
            suggestions.append({
                "source_column": col,
                "suggestion": "text_length",
                "description": f"Add '{col}_len' as character count of '{col}'.",
                "new_features": [f"{col}_len"],
            })

    # Interaction terms for numeric pairs
    numeric_cols = [
        col for col in df.columns
        if df[col].dtype in (pl.Float64, pl.Float32, pl.Int64, pl.Int32)
    ]
    if len(numeric_cols) >= 2:
        a, b = numeric_cols[0], numeric_cols[1]
        suggestions.append({
            "source_column": f"{a}, {b}",
            "suggestion": "interaction_term",
            "description": f"Create interaction feature '{a}_x_{b}' = {a} * {b}.",
            "new_features": [f"{a}_x_{b}"],
        })

    return suggestions
