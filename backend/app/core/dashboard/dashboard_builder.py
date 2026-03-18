import polars as pl
from typing import List, Dict, Any
from app.utils.logger import get_logger

logger = get_logger(__name__)


def build_dashboard(dataset_id: str, df: pl.DataFrame, charts: List[Dict[str, Any]]) -> Dict:
    """
    Builds a dashboard spec. Attempts Superset if available, else returns local spec.
    """
    try:
        from app.core.dashboard.superset_client import SupersetClient
        client = SupersetClient()
        client.login()
        url = client.create_dashboard(
            title=f"DataSherlock - {dataset_id}",
            chart_ids=[],
        )
        logger.info(f"Superset dashboard created: {url}")
        return {"url": url, "source": "superset"}
    except Exception as e:
        logger.warning(f"Superset unavailable ({e}), returning local chart spec.")
        return {
            "url": f"/api/v1/dashboard/{dataset_id}/local",
            "source": "local",
            "charts": charts,
        }
