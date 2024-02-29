import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from app.config import settings


def setup_sentry() -> None:
    """Set up Sentry error reporting and monitoring."""
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        traces_sample_rate=settings.sentry_sample_rate,
        integrations=[
            LoggingIntegration(
                level=logging.getLevelName(
                    level=settings.log_level,
                ),
                event_level=logging.ERROR,
            ),
        ],
    )
