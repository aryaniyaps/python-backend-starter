import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from app.config import settings


def setup_sentry() -> None:
    """Set up Sentry error reporting and monitoring."""
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        debug=settings.debug,
        traces_sample_rate=settings.sentry_sample_rate,
        integrations=[
            StarletteIntegration(
                transaction_style="url",
            ),
            FastApiIntegration(
                transaction_style="url",
            ),
            # disable standard library logging
            # FIXME: not sure if this is needed, we could keep this integration
            # and remove the structlog-sentry processor instead
            LoggingIntegration(
                level=None,
                event_level=None,
            ),
        ],
    )
