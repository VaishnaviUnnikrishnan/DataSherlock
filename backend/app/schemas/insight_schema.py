from pydantic import BaseModel
from typing import List, Dict, Any


class InsightResponse(BaseModel):
    dataset_id: str
    rule_insights: List[Dict[str, Any]]
    root_causes: List[Dict[str, Any]]
    feature_suggestions: List[Dict[str, Any]]
