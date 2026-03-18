from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.core.profiling.dqi import compute_dqi
from app.core.profiling.missing_analysis import analyze_missing
from app.core.profiling.outlier_detection import detect_outliers
from app.core.profiling.correlation import compute_correlation
from app.core.profiling.drift_detection import detect_drift
from app.core.ingestion.loader import DataLoader
from app.db.duckdb_connection import get_db
from app.schemas.profiling_schema import ProfilingResponse
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


def _get_df(dataset_id: str):
    db = get_db()
    row = db.execute("SELECT file_path FROM datasets WHERE id = ?", [dataset_id]).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return DataLoader(row[0]).load()


@router.get("/{dataset_id}", response_model=ProfilingResponse)
async def profile_dataset(dataset_id: str):
    df = _get_df(dataset_id)
    missing = analyze_missing(df)
    outliers = detect_outliers(df)
    correlation = compute_correlation(df)
    dqi = compute_dqi(df, missing, outliers)

    logger.info(f"Profiling complete for {dataset_id}, DQI={dqi['score']:.2f}")
    return ProfilingResponse(
        dataset_id=dataset_id,
        dqi=dqi,
        missing=missing,
        outliers=outliers,
        correlation=correlation,
    )


@router.get("/{dataset_id}/drift")
async def drift_report(dataset_id: str, reference_id: str):
    df_current = _get_df(dataset_id)
    df_reference = _get_df(reference_id)
    drift = detect_drift(df_reference, df_current)
    return {"dataset_id": dataset_id, "reference_id": reference_id, "drift": drift}
