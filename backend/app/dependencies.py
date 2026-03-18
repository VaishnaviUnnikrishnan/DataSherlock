from app.db.duckdb_connection import get_db
from fastapi import Depends
import duckdb


def get_database() -> duckdb.DuckDBPyConnection:
    return get_db()
