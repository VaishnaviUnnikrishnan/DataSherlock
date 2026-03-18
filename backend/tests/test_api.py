import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_upload_csv():
    csv_content = b"id,name,sales\n1,Alice,100\n2,Bob,200\n3,Charlie,150\n"
    resp = client.post(
        "/api/v1/upload/",
        files={"file": ("test.csv", io.BytesIO(csv_content), "text/csv")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["rows"] == 3
    assert data["columns"] == 3
    assert "dataset_id" in data
    return data["dataset_id"]


def test_profiling_after_upload():
    dataset_id = test_upload_csv()
    resp = client.get(f"/api/v1/profiling/{dataset_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert "dqi" in data
    assert data["dqi"]["score"] >= 0
