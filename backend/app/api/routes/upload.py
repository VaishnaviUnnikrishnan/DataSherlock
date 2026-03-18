from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.core.ingestion.loader import DataLoader
from app.core.ingestion.validators import validate_file
from app.core.ingestion.schema_inference import infer_schema
from app.schemas.upload_schema import UploadResponse
from app.db.duckdb_connection import get_db
from app.utils.logger import get_logger
import uuid, os, shutil
from app.config import settings

router = APIRouter()
logger = get_logger(__name__)


@router.post("/", response_model=UploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    validate_file(file)
    dataset_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[-1].lower()
    save_path = os.path.join(settings.UPLOAD_DIR, f"{dataset_id}{ext}")

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    loader = DataLoader(save_path)
    df = loader.load()
    schema = infer_schema(df)

    db = get_db()
    db.execute(
        "INSERT INTO datasets VALUES (?, ?, ?, ?, ?)",
        [dataset_id, file.filename, save_path, str(schema), "uploaded"],
    )

    logger.info(f"Uploaded dataset {dataset_id}: {file.filename}")
    return UploadResponse(
        dataset_id=dataset_id,
        filename=file.filename,
        rows=df.shape[0],
        columns=df.shape[1],
        schema=schema,
        status="uploaded",
    )


@router.get("/{dataset_id}")
async def get_dataset_info(dataset_id: str):
    db = get_db()
    result = db.execute(
        "SELECT * FROM datasets WHERE id = ?", [dataset_id]
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return {"dataset_id": result[0], "filename": result[1], "status": result[4]}
