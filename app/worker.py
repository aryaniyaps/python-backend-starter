from celery import Celery

from app.config import Settings


def create_worker(settings: Settings) -> Celery:
    """Initialize a worker instance."""
    celery = Celery(__name__)
    celery.conf.update(
        {
            "broker_url": str(settings.celery_broker_url),
            "imports": ("app.auth.tasks",),
        }
    )
    return celery


worker = create_worker(
    settings=Settings(),  # type: ignore
)
