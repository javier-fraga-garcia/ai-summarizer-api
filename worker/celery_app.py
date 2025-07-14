from celery import Celery

from core.config import settings

celery_app = Celery("summarizer_app", broker=settings.CELERY_BROKER)
celery_app.autodiscover_tasks(['worker.tasks'])

from worker.tasks import scrape, summarize