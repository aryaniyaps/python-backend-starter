from celery import Celery

from app.config import CELERY_BROKER_URL


def create_worker() -> Celery:
    """Initialize a worker instance."""
    celery = Celery(__name__)
    celery.conf.update(
        {
            "broker_url": CELERY_BROKER_URL,
            "imports": ("emails.tasks",),
        }
    )
    celery.autodiscover_tasks()
    return celery


worker = create_worker()
