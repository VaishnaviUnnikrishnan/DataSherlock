from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "DataSherlock"
    APP_ENV: str = "development"
    DEBUG: bool = True

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama3-70b-8192"

    REDIS_URL: str = "redis://localhost:6379/0"
    DUCKDB_PATH: str = "./data/datasherlock.duckdb"

    SUPERSET_URL: str = "http://localhost:8088"
    SUPERSET_USERNAME: str = "admin"
    SUPERSET_PASSWORD: str = "admin"

    MAX_UPLOAD_SIZE_MB: int = 100
    UPLOAD_DIR: str = "./data/uploads"

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
