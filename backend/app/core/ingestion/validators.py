from fastapi import UploadFile, HTTPException
from app.config import settings

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".json", ".parquet"}
MAX_SIZE_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


def validate_file(file: UploadFile):
    import os
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: {ALLOWED_EXTENSIONS}",
        )
