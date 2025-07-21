from pydantic import BaseModel
from datetime import datetime


class JobRequest(BaseModel):
    url: str


class JobResponse(BaseModel):
    url: str
    created_at: datetime
    job_id: str
    status: str = "pending"

    model_config = {"from_attributes": True}


class JobStatusResponse(BaseModel):
    job_id: str
    status: str

    model_config = {"from_attributes": True}


class JobCompletedResponse(JobResponse):
    id: int
    completed_at: datetime
    summary: str
    audio_url: str | None

    model_config = {"from_attributes": True}
