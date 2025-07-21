from worker.celery_app import celery_app
from db.database import SessionLocal
from models.job import SummaryJob
from core.scraper import Scraper

from core.logger import get_logger

logger = get_logger(__name__)


@celery_app.task(name="scrape_url")
def scrape_url(url: str, job_id: str) -> dict:
    db = SessionLocal()

    try:
        job = db.query(SummaryJob).filter(SummaryJob.job_id == job_id).first()
        if not job:
            raise ValueError(f"Job with id #{job_id} not found")

        content = Scraper.scrape(url)
        job.status = "scraped"
        db.commit()
        return {"content": content, "job_id": job_id}

    except Exception as e:
        logger.error(e)
        if job:
            job.status = "failed"
            db.commit()
        raise

    finally:
        db.close()
