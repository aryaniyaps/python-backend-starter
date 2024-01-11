from celery import Celery

from app.config import settings


def create_worker() -> Celery:
    """Initialize a worker instance."""
    celery = Celery(__name__)
    celery.conf.update(
        {
            "broker_url": str(settings.celery_broker_url),
            "imports": ("app.auth.tasks",),
        }
    )

    return celery


worker = create_worker()
