import dramatiq
from dramatiq.brokers.redis import RedisBroker

from app.auth.actors import send_password_reset_request_email
from app.config import settings

__all__ = (
    "send_password_reset_request_email",
    "setup_broker",
)


def setup_broker() -> None:
    """Configure the dramatiq broker."""
    dramatiq.set_broker(
        broker=RedisBroker(
            url=str(settings.dramatiq_broker_url),
        )  # type: ignore[no-untyped-call]
    )
