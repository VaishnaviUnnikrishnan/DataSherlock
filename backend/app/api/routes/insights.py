from fastapi import APIRouter, HTTPException
from app.core.insights.rule_engine import run_rule_engine
from app.core.insights.root_cause import analyze_root_cause
from app.core.insights.feature_suggestions import suggest_features
from app.core.ingestion.loader import DataLoader
from app.db.duckdb_connection import get_db
from app.schemas.insight_schema import InsightResponse
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


def _get_df(dataset_id: str):
    db = get_db()
    row = db.execute("SELECT file_path FROM datasets WHERE id = ?", [dataset_id]).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return DataLoader(row[0]).load()


@router.get("/{dataset_id}", response_model=InsightResponse)
async def get_insights(dataset_id: str):
    df = _get_df(dataset_id)
    rules = run_rule_engine(df)
    root_causes = analyze_root_cause(df)
    features = suggest_features(df)

    logger.info(f"Insights generated for {dataset_id}")
    return InsightResponse(
        dataset_id=dataset_id,
        rule_insights=rules,
        root_causes=root_causes,
        feature_suggestions=features,
    )
