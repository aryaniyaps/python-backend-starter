import logging

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from app.config import settings


def _get_sentry_environment() -> str:
    """Get the Sentry environment."""
    if settings.debug:
        return "development"
    return "production"


def setup_sentry() -> None:
    """Set up Sentry error reporting and monitoring."""
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=_get_sentry_environment(),
        debug=settings.debug,
        traces_sample_rate=settings.sentry_sample_rate,
        integrations=[
            LoggingIntegration(
                level=logging.getLevelName(
                    settings.log_level,
                ),
                event_level=logging.ERROR,
            ),
            StarletteIntegration(
                transaction_style="url",
            ),
            FastApiIntegration(
                transaction_style="url",
            ),
        ],
    )
