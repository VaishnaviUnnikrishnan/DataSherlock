from pydantic import BaseModel
from typing import List, Dict, Any


class DashboardResponse(BaseModel):
    dataset_id: str
    dashboard_url: str
    charts: List[Dict[str, Any]]
    status: str
