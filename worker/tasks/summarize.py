from datetime import datetime, timezone
from worker.celery_app import celery_app
from db.database import SessionLocal
from models.job import SummaryJob
import time


@celery_app.task(name='summarize')
def summarize(data: dict) -> dict:
    db = SessionLocal()
    try:
        summary = "Text summary"
        job = db.query(SummaryJob).filter(SummaryJob.job_id == data.get('job_id')).first()
        job.status = "summarized"
        job.summary = summary
        job.completed_at = datetime.now(timezone.utc)
        db.flush()
        db.commit()

        time.sleep(60 * 2)
        return {"summary": summary, "job_id": data.get('job_id')}
    finally:
        db.close()
