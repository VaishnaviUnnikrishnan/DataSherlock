from pydantic import BaseModel
from typing import Dict, Any


class ProfilingResponse(BaseModel):
    dataset_id: str
    dqi: Dict[str, Any]
    missing: Dict[str, Any]
    outliers: Dict[str, Any]
    correlation: Dict[str, Any]
