from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from db.database import Base


class SummaryJob(Base):
    __tablename__ = "summary_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    url = Column(Text)
    summary = Column(Text, nullable=True)
    audio_url = Column(Text, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
