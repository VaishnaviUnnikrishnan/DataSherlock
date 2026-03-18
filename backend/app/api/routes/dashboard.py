from fastapi import APIRouter, HTTPException
from app.core.dashboard.chart_selector import select_charts
from app.core.dashboard.dashboard_builder import build_dashboard
from app.core.ingestion.loader import DataLoader
from app.db.duckdb_connection import get_db
from app.schemas.dashboard_schema import DashboardResponse
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/{dataset_id}/generate", response_model=DashboardResponse)
async def generate_dashboard(dataset_id: str):
    db = get_db()
    row = db.execute("SELECT file_path FROM datasets WHERE id = ?", [dataset_id]).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = DataLoader(row[0]).load()
    charts = select_charts(df)
    result = build_dashboard(dataset_id, df, charts)

    logger.info(f"Dashboard generated for {dataset_id}")
    return DashboardResponse(
        dataset_id=dataset_id,
        dashboard_url=result.get("url", ""),
        charts=charts,
        status="created",
    )
