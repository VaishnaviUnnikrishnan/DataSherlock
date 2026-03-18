import requests
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SupersetClient:
    def __init__(self):
        self.base_url = settings.SUPERSET_URL
        self.token = None

    def login(self):
        resp = requests.post(
            f"{self.base_url}/api/v1/security/login",
            json={
                "username": settings.SUPERSET_USERNAME,
                "password": settings.SUPERSET_PASSWORD,
                "provider": "db",
            },
        )
        resp.raise_for_status()
        self.token = resp.json()["access_token"]
        logger.info("Superset login successful")

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def create_dataset(self, table_name: str, database_id: int = 1) -> int:
        resp = requests.post(
            f"{self.base_url}/api/v1/dataset/",
            json={"database": database_id, "table_name": table_name, "schema": "main"},
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()["id"]

    def create_chart(self, chart_config: dict) -> int:
        resp = requests.post(
            f"{self.base_url}/api/v1/chart/",
            json=chart_config,
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()["id"]

    def create_dashboard(self, title: str, chart_ids: list) -> str:
        resp = requests.post(
            f"{self.base_url}/api/v1/dashboard/",
            json={"dashboard_title": title, "published": True},
            headers=self._headers(),
        )
        resp.raise_for_status()
        dashboard_id = resp.json()["id"]
        return f"{self.base_url}/superset/dashboard/{dashboard_id}/"
