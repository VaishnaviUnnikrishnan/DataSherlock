from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.config import settings
from app.db.duckdb_connection import init_db
from app.utils.logger import get_logger
import os

logger = get_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous Agentic Data Intelligence & Dashboard Automation System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    init_db()
    logger.info(f"{settings.APP_NAME} started successfully.")


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "app": settings.APP_NAME}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}


app.include_router(api_router, prefix="/api/v1")
