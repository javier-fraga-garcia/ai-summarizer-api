from datetime import datetime, timezone
import time

from worker.celery_app import celery_app
from db.database import SessionLocal
from models.job import SummaryJob


@celery_app.task(name="summarize")
def summarize(data: dict) -> dict:
    time.sleep(60 * 2)
    db = SessionLocal()
    try:
        summary = "Text summary"
        job = (
            db.query(SummaryJob).filter(SummaryJob.job_id == data.get("job_id")).first()
        )
        job.status = "summarized"
        job.summary = summary
        job.completed_at = datetime.now(timezone.utc)
        db.flush()
        db.commit()

        return {"summary": summary, "job_id": data.get("job_id")}
    finally:
        db.close()
