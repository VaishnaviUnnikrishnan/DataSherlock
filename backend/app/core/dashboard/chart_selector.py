import polars as pl
from typing import List, Dict, Any


def select_charts(df: pl.DataFrame) -> List[Dict[str, Any]]:
    charts = []
    numeric_cols = [
        col for col in df.columns
        if df[col].dtype in (pl.Float64, pl.Float32, pl.Int64, pl.Int32)
    ]
    categorical_cols = [
        col for col in df.columns
        if df[col].dtype in (pl.Utf8, pl.String) and df[col].n_unique() < 20
    ]
    time_cols = [
        col for col in df.columns
        if any(k in col.lower() for k in ["date", "time", "timestamp"])
    ]

    # Bar chart for categoricals
    for col in categorical_cols[:3]:
        charts.append({
            "type": "bar",
            "x": col,
            "y": "count",
            "title": f"Distribution of {col}",
        })

    # Histogram for numerics
    for col in numeric_cols[:3]:
        charts.append({
            "type": "histogram",
            "x": col,
            "title": f"Distribution of {col}",
        })

    # Line chart for time series
    for tcol in time_cols[:1]:
        for ncol in numeric_cols[:1]:
            charts.append({
                "type": "line",
                "x": tcol,
                "y": ncol,
                "title": f"{ncol} over time",
            })

    # Scatter plot for correlated numeric pairs
    if len(numeric_cols) >= 2:
        charts.append({
            "type": "scatter",
            "x": numeric_cols[0],
            "y": numeric_cols[1],
            "title": f"{numeric_cols[0]} vs {numeric_cols[1]}",
        })

    return charts
