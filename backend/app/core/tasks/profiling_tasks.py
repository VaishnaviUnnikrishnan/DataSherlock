import dramatiq
from app.core.tasks.celery_app import redis_broker  # ensures broker is set
from app.core.ingestion.loader import DataLoader
from app.core.profiling.dqi import compute_dqi
from app.core.profiling.missing_analysis import analyze_missing
from app.core.profiling.outlier_detection import detect_outliers
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dramatiq.actor
def run_full_profile(dataset_id: str, file_path: str):
    logger.info(f"[Task] Starting full profile for {dataset_id}")
    try:
        df = DataLoader(file_path).load()
        missing = analyze_missing(df)
        outliers = detect_outliers(df)
        dqi = compute_dqi(df, missing, outliers)
        logger.info(f"[Task] Profiling done for {dataset_id}, DQI={dqi['score']}")
    except Exception as e:
        logger.error(f"[Task] Profiling failed for {dataset_id}: {e}")
