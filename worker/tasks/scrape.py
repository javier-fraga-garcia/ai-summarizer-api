from worker.celery_app import celery_app
from db.database import SessionLocal
from models.job import SummaryJob
import time


@celery_app.task(name='scrape_url')
def scrape_url(url: str, job_id: str) -> dict:
    time.sleep(60)
    db = SessionLocal()
    try:
        job = db.query(SummaryJob).filter(SummaryJob.job_id == job_id).first()
        print(job_id)
        job.status = "scraped"
        db.flush()
        db.commit()
        return {"content": "Text content", "job_id": job_id}
    finally:
        db.close()
