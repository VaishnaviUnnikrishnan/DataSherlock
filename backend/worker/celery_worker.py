"""
DataSherlock Dramatiq Worker
Run with: dramatiq worker.celery_worker
"""
from app.core.tasks.celery_app import redis_broker  # noqa: F401 - sets broker
from app.core.tasks.profiling_tasks import run_full_profile  # noqa: F401 - registers actors

if __name__ == "__main__":
    print("Worker registered. Run via: dramatiq worker.celery_worker")
