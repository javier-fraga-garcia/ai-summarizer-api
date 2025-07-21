import os
from datetime import datetime, timezone

from worker.celery_app import celery_app
from db.database import SessionLocal
from models.job import SummaryJob
from core.logger import get_logger
from core.storage import StorageService

logger = get_logger(__name__)


@celery_app.task(name="store")
def store(data: dict) -> None:
    db = SessionLocal()

    try:
        job_id = data.get("job_id")
        results = StorageService.store(data.get("file_path"))
        job = db.query(SummaryJob).filter(SummaryJob.job_id == job_id).first()
        if not job:
            raise ValueError(f"Job with id #{job_id} not found")

        job.status = "completed"
        job.completed_at = datetime.now(timezone.utc)
        job.audio_url = results.get("presigned_url")
        job.file_key = results.get("file_key")
        db.commit()

        os.remove(data.get("file_path"))

    except Exception as e:
        logger.error(e)
        if job:
            job.status = "failed"
        raise

    finally:
        db.close()
