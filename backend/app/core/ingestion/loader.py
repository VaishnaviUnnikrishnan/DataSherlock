import polars as pl
import os
from app.utils.logger import get_logger

logger = get_logger(__name__)

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".json", ".parquet"}


class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.ext = os.path.splitext(file_path)[-1].lower()

    def load(self) -> pl.DataFrame:
        logger.info(f"Loading file: {self.file_path}")
        if self.ext == ".csv":
            return pl.read_csv(self.file_path, infer_schema_length=1000)
        elif self.ext == ".xlsx":
            return pl.read_excel(self.file_path)
        elif self.ext == ".json":
            return pl.read_json(self.file_path)
        elif self.ext == ".parquet":
            return pl.read_parquet(self.file_path)
        else:
            raise ValueError(f"Unsupported file extension: {self.ext}")
