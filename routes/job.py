from uuid import uuid4
from celery import chain
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from core.config import settings
from schemas.job import JobRequest, JobResponse, JobStatusResponse, JobCompletedResponse
from models.job import SummaryJob
from worker.tasks.scrape import scrape_url
from worker.tasks.summarize import summarize

router = APIRouter(prefix=f"{settings.API_PREFIX}/jobs", tags=["jobs"])


@router.post("/", response_model=JobResponse)
def create_job(request: JobRequest, db: Session = Depends(get_db)):
    try:
        job_id = str(uuid4())
        job = SummaryJob(job_id=job_id, url=request.url)
        db.add(job)
        db.commit()

        chain(scrape_url.s(request.url, job_id), summarize.s()).apply_async()
        return job
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/{job_id}/status", response_model=JobStatusResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    try:
        job = db.query(SummaryJob).filter(SummaryJob.job_id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=404, detail=f"Job with id #{job_id} not found"
            )
        return job
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/{job_id}/completed", response_model=JobCompletedResponse)
def get_completed_job(job_id: str, db: Session = Depends(get_db)):
    # TODO: implement logic to return only completed jobs
    try:
        job = db.query(SummaryJob).filter(SummaryJob.job_id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=404, detail=f"Job with id #{job_id} not found"
            )
        return job
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")
