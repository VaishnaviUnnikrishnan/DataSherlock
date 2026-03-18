from fastapi import APIRouter
from app.api.routes import upload, profiling, insights, ask, dashboard

api_router = APIRouter()

api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
api_router.include_router(profiling.router, prefix="/profiling", tags=["Profiling"])
api_router.include_router(insights.router, prefix="/insights", tags=["Insights"])
api_router.include_router(ask.router, prefix="/ask", tags=["Ask AI"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
