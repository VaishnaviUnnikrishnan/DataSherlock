import polars as pl
import pytest
from app.core.profiling.missing_analysis import analyze_missing
from app.core.profiling.outlier_detection import detect_outliers
from app.core.profiling.dqi import compute_dqi
from app.core.profiling.correlation import compute_correlation


@pytest.fixture
def sample_df():
    return pl.DataFrame({
        "a": [1.0, 2.0, None, 4.0, 100.0],
        "b": [10.0, 20.0, 30.0, 40.0, 50.0],
        "c": ["x", "y", "x", None, "z"],
    })


def test_missing_analysis(sample_df):
    result = analyze_missing(sample_df)
    assert result["a"]["missing_count"] == 1
    assert result["c"]["missing_pct"] == 20.0


def test_outlier_detection(sample_df):
    result = detect_outliers(sample_df)
    assert "a" in result
    assert result["a"]["outlier_count"] >= 1


def test_dqi(sample_df):
    missing = analyze_missing(sample_df)
    outliers = detect_outliers(sample_df)
    dqi = compute_dqi(sample_df, missing, outliers)
    assert 0 <= dqi["score"] <= 100
    assert dqi["grade"] in ("A", "B", "C", "D", "F")


def test_correlation(sample_df):
    result = compute_correlation(sample_df)
    assert "matrix" in result
    assert "strong_pairs" in result
