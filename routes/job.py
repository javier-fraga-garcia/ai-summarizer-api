from uuid import uuid4
from celery import chain
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from core.config import settings
from schemas.job import JobRequest, JobResponse
from models.job import SummaryJob
from worker.tasks.scrape import scrape_url
from worker.tasks.summarize import summarize
from worker.celery_app import celery_app

router = APIRouter(prefix=f"{settings.API_PREFIX}/jobs", tags=["jobs"])


@router.post("/", response_model=JobResponse)
def create_job(request: JobRequest, db: Session = Depends(get_db)):
    try:
        job_id = str(uuid4())
        job = SummaryJob(job_id=job_id, url=request.url)
        db.add(job)
        db.commit()

        celery_job = chain(
            scrape_url.s(request.url, job_id),
            summarize.s()
        ).apply_async()
        return job
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Something went wrong')
