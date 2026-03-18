from app.utils.constants import DOMAIN_KEYWORDS
from typing import Optional
import polars as pl


def detect_domain(df: pl.DataFrame) -> Optional[str]:
    """Infer data domain from column names."""
    col_names = " ".join(df.columns).lower()
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        scores[domain] = sum(1 for k in keywords if k in col_names)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else None


def safe_json(obj):
    """Convert objects to JSON-safe types."""
    if hasattr(obj, "item"):
        return obj.item()
    if isinstance(obj, dict):
        return {k: safe_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [safe_json(i) for i in obj]
    return obj
