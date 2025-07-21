from worker.celery_app import celery_app
from db.database import SessionLocal
from models.job import SummaryJob
from core.audio_generator import AudioGenerator
from core.logger import get_logger

logger = get_logger(__name__)


@celery_app.task(name="generate_audio")
def generate_audio(data: dict) -> dict:
    db = SessionLocal()

    try:
        job_id = data.get("job_id")
        tmp_file_path = AudioGenerator.generate_audio_file(data.get("summary"), job_id)
        job = db.query(SummaryJob).filter(SummaryJob.job_id == job_id).first()
        if not job:
            raise ValueError(f"Job with id #{job_id} not found")

        job.status = "audio_generated"
        db.commit()
        return {"file_path": str(tmp_file_path), "job_id": job_id}

    except Exception as e:
        logger.error(e)
        if job:
            job.status = "failed"
        raise

    finally:
        db.close()
