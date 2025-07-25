from worker.celery_app import celery_app
from db.database import SessionLocal
from models.job import SummaryJob
from core.summarizer import Summarizer
from core.logger import get_logger

logger = get_logger(__name__)


@celery_app.task(name="summarize")
def summarize(data: dict) -> dict:
    db = SessionLocal()

    try:
        job_id = data.get("job_id")
        summary = Summarizer.summarize(data.get("content"))
        job = db.query(SummaryJob).filter(SummaryJob.job_id == job_id).first()
        if not job:
            raise ValueError(f"Job with id #{job_id} not found")

        job.status = "summarized"
        job.summary = summary
        db.commit()

        return {"summary": summary, "job_id": job_id}
    except Exception as e:
        logger.error(e)
        if job:
            job.status = "failed"
        raise

    finally:
        db.close()
