from pydantic import BaseModel
from typing import Dict, Any


class UploadResponse(BaseModel):
    dataset_id: str
    filename: str
    rows: int
    columns: int
    schema: Dict[str, Any]
    status: str
