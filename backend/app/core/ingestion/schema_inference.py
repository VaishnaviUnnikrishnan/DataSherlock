import polars as pl
from typing import Dict, Any

TIME_KEYWORDS = ["date", "time", "timestamp", "created", "updated", "at", "on"]
ID_KEYWORDS = ["id", "key", "uuid", "pk", "fk"]


def infer_schema(df: pl.DataFrame) -> Dict[str, Any]:
    schema = {}
    for col in df.columns:
        dtype = str(df[col].dtype)
        col_lower = col.lower()

        is_temporal = any(k in col_lower for k in TIME_KEYWORDS)
        is_id = any(k in col_lower for k in ID_KEYWORDS)
        n_unique = df[col].n_unique()
        is_categorical = (
            dtype in ("Utf8", "String") and n_unique < 50
        )

        schema[col] = {
            "dtype": dtype,
            "nullable": df[col].null_count() > 0,
            "n_unique": n_unique,
            "is_temporal": is_temporal,
            "is_id_column": is_id,
            "is_categorical": is_categorical,
        }
    return schema
