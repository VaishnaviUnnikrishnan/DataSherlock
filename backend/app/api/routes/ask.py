from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.llm.agent_graph import run_agent
from app.core.ingestion.loader import DataLoader
from app.db.duckdb_connection import get_db
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


class AskRequest(BaseModel):
    dataset_id: str
    question: str


class AskResponse(BaseModel):
    dataset_id: str
    question: str
    answer: str


@router.post("/", response_model=AskResponse)
async def ask_question(payload: AskRequest):
    db = get_db()
    row = db.execute(
        "SELECT file_path, schema_info FROM datasets WHERE id = ?",
        [payload.dataset_id],
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = DataLoader(row[0]).load()
    answer = run_agent(question=payload.question, df=df, schema_info=row[1])

    logger.info(f"Ask query answered for dataset {payload.dataset_id}")
    return AskResponse(
        dataset_id=payload.dataset_id,
        question=payload.question,
        answer=answer,
    )
