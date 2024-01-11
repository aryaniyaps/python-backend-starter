from celery import Celery
from celery.signals import worker_init, worker_shutdown

from app.config import settings
from app.core.emails import mailer


@worker_init.connect
def start_mailer() -> None:
    """Start the mailer."""
    mailer.start()


@worker_shutdown.connect
def shutdown_mailer() -> None:
    """Shutdown the mailer."""
    mailer.stop()


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
