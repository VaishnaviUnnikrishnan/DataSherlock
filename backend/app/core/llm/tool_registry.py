import polars as pl
import numpy as np
from langchain.tools import tool

_df_store: dict[str, pl.DataFrame] = {}


def register_df(key: str, df: pl.DataFrame):
    _df_store[key] = df


def _get_df() -> pl.DataFrame:
    if not _df_store:
        raise ValueError("No dataset loaded.")
    return next(iter(_df_store.values()))


@tool
def get_dataset_shape(dummy: str = "") -> str:
    """Returns the number of rows and columns in the loaded dataset."""
    df = _get_df()
    return f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns."


@tool
def list_columns(dummy: str = "") -> str:
    """Lists all column names and their data types."""
    df = _get_df()
    return "\n".join([f"  - {col}: {df[col].dtype}" for col in df.columns])


@tool
def get_column_stats(col_name: str) -> str:
    """Returns descriptive statistics (mean, std, min, max, nulls) for a numeric column."""
    df = _get_df()
    if col_name not in df.columns:
        return f"Column '{col_name}' not found. Available: {', '.join(df.columns)}"
    s = df[col_name]
    null_count = s.null_count()
    s_clean = s.drop_nulls()
    if s.dtype not in (pl.Float64, pl.Float32, pl.Int64, pl.Int32, pl.Int16, pl.Int8):
        return f"Column '{col_name}' is not numeric (dtype={s.dtype}). Use get_value_counts instead."
    return (
        f"Column '{col_name}' stats:\n"
        f"  mean={s_clean.mean():.4f}, std={s_clean.std():.4f}\n"
        f"  min={s_clean.min()}, max={s_clean.max()}\n"
        f"  nulls={null_count} ({null_count/df.shape[0]*100:.1f}%)"
    )


@tool
def get_value_counts(col_name: str) -> str:
    """Returns the top 10 value counts for a categorical or string column."""
    df = _get_df()
    if col_name not in df.columns:
        return f"Column '{col_name}' not found."
    counts = df[col_name].value_counts().sort("count", descending=True).head(10)
    lines = [f"  {row[col_name]}: {row['count']}" for row in counts.to_dicts()]
    return f"Top values in '{col_name}':\n" + "\n".join(lines)


@tool
def get_missing_summary(dummy: str = "") -> str:
    """Returns a summary of missing values across all columns."""
    df = _get_df()
    lines = []
    for col in df.columns:
        n = df[col].null_count()
        if n > 0:
            pct = n / df.shape[0] * 100
            lines.append(f"  {col}: {n} missing ({pct:.1f}%)")
    return "Missing value summary:\n" + ("\n".join(lines) if lines else "  No missing values found.")


@tool
def detect_outliers_tool(col_name: str) -> str:
    """Detects outliers in a numeric column using the IQR method."""
    df = _get_df()
    if col_name not in df.columns:
        return f"Column '{col_name}' not found."
    s = df[col_name].drop_nulls()
    if df[col_name].dtype not in (pl.Float64, pl.Float32, pl.Int64, pl.Int32):
        return f"Column '{col_name}' is not numeric."
    arr = s.to_numpy()
    q1, q3 = np.percentile(arr, 25), np.percentile(arr, 75)
    iqr = q3 - q1
    outliers = int(((arr < q1 - 1.5 * iqr) | (arr > q3 + 1.5 * iqr)).sum())
    return (
        f"Outlier analysis for '{col_name}':\n"
        f"  IQR range: [{q1 - 1.5*iqr:.4f}, {q3 + 1.5*iqr:.4f}]\n"
        f"  Outliers found: {outliers} ({outliers/len(arr)*100:.1f}% of non-null values)"
    )


@tool
def get_correlation_pairs(dummy: str = "") -> str:
    """Returns strongly correlated numeric column pairs (|correlation| >= 0.7)."""
    df = _get_df()
    num_cols = [c for c in df.columns if df[c].dtype in (pl.Float64, pl.Float32, pl.Int64, pl.Int32)]
    if len(num_cols) < 2:
        return "Not enough numeric columns for correlation analysis."
    arr = df.select(num_cols).drop_nulls().to_numpy()
    corr = np.corrcoef(arr.T)
    pairs = []
    for i in range(len(num_cols)):
        for j in range(i + 1, len(num_cols)):
            if abs(corr[i, j]) >= 0.7:
                pairs.append(f"  {num_cols[i]} ↔ {num_cols[j]}: {corr[i,j]:.4f}")
    return "Strong correlations (|r| ≥ 0.7):\n" + ("\n".join(pairs) if pairs else "  None found.")


@tool
def get_data_sample(n: str = "5") -> str:
    """Returns the first N rows of the dataset as a readable table. Pass n as a string number."""
    df = _get_df()
    try:
        n_int = int(n)
    except ValueError:
        n_int = 5
    return df.head(n_int).to_pandas().to_string(index=False)


TOOLS = [
    get_dataset_shape,
    list_columns,
    get_column_stats,
    get_value_counts,
    get_missing_summary,
    detect_outliers_tool,
    get_correlation_pairs,
    get_data_sample,
]