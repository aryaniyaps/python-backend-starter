from typing import Any

import structlog
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer
from structlog.types import EventDict, Processor, WrappedLogger

from app.config import settings


def remove_color_message(
    _logger: WrappedLogger, _method_name: str, event_dict: EventDict
) -> EventDict:
    """
    remove `color_message` from the event dict.

    Uvicorn logs the message a second time in the extra `color_message`, but we don't
    need it. This processor removes the key from the event dict if it exists.
    """
    event_dict.pop("color_message", None)
    return event_dict


def get_logging_renderer() -> JSONRenderer | ConsoleRenderer:
    """Get the logging renderer."""
    if settings.debug:
        return ConsoleRenderer()
    return JSONRenderer(indent=1, sort_keys=True)


def build_shared_processors(*, human_readable: bool) -> list[Processor]:
    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,  # Merge context variables
        structlog.stdlib.add_log_level,  # Add log level
        structlog.stdlib.add_logger_name,  # Add logger name
        structlog.stdlib.PositionalArgumentsFormatter(),  # Add positional arguments
        structlog.processors.StackInfoRenderer(),  # Add stack information
        structlog.stdlib.ExtraAdder(),  # Add extra attributes
        remove_color_message,  # Drop color message
        timestamper,  # Add timestamps
    ]

    if not human_readable:
        # Format the exception only in production
        # (we want to pretty-print them when using the ConsoleRenderer in development)
        shared_processors.append(structlog.processors.format_exc_info)
    return shared_processors


# TODO: build log config for server and worker separately
def build_log_config(log_level: str, *, human_readable: bool) -> dict[str, Any]:
    """Build application logging config."""
    # Define custom logging configuration
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structlog": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    get_logging_renderer(),
                ],
                "foreign_pre_chain": build_shared_processors(
                    human_readable=human_readable,
                ),
            },
        },
        "handlers": {
            "default": {
                "formatter": "structlog",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "fastapi": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "rq.worker": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "sqlalchemy": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
        },
    }


def setup_logging(*, human_readable: bool) -> None:
    """Set up application logging."""
    structlog_processors = [
        *build_shared_processors(
            human_readable=human_readable,
        ),
        # Prepare event dict for `ProcessorFormatter`.
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure_once(
        processors=structlog_processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
