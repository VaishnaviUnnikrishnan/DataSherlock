import duckdb
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

_conn: duckdb.DuckDBPyConnection = None


def get_db() -> duckdb.DuckDBPyConnection:
    global _conn
    if _conn is None:
        _conn = duckdb.connect(settings.DUCKDB_PATH)
    return _conn


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id VARCHAR PRIMARY KEY,
            filename VARCHAR,
            file_path VARCHAR,
            schema_info VARCHAR,
            status VARCHAR
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS profiling_results (
            dataset_id VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            dqi_score FLOAT,
            result_json VARCHAR
        )
    """)
    logger.info("DuckDB initialized.")
