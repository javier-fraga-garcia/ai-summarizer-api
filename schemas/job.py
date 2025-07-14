from pydantic import BaseModel
from datetime import datetime


class JobRequest(BaseModel):
    url: str
    audio: bool = False


class JobResponse(BaseModel):
    url: str
    created_at: datetime
    job_id: str
    status: str = "pending"

    model_config = {"from_attributes": True}
