import pytest
import polars as pl
import os
import tempfile
from app.core.ingestion.loader import DataLoader
from app.core.ingestion.schema_inference import infer_schema


@pytest.fixture
def sample_csv():
    df = pl.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "sales": [100.0, 200.5, 150.0],
        "created_at": ["2024-01-01", "2024-01-02", "2024-01-03"],
    })
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
        df.write_csv(f.name)
        return f.name


def test_csv_load(sample_csv):
    loader = DataLoader(sample_csv)
    df = loader.load()
    assert df.shape == (3, 4)
    os.unlink(sample_csv)


def test_schema_inference(sample_csv):
    loader = DataLoader(sample_csv)
    df = loader.load()
    schema = infer_schema(df)
    assert "id" in schema
    assert schema["id"]["is_id_column"] is True
    assert schema["created_at"]["is_temporal"] is True
