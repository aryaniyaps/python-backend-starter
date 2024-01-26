from logging import StreamHandler
from logging.config import dictConfig
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


def get_renderer() -> JSONRenderer | ConsoleRenderer:
    """Get the logging renderer."""
    return JSONRenderer(indent=1, sort_keys=True)
    # if settings.debug:
    #     return ConsoleRenderer()
    # return JSONRenderer(indent=1, sort_keys=True)


def setup_logging(log_level: str) -> None:
    """Set up application logging."""
    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
    shared_processors: list[Processor] = [
        structlog.stdlib.add_log_level,  # Add log level
        structlog.contextvars.merge_contextvars,  # Merge context variables
        structlog.stdlib.PositionalArgumentsFormatter(),  # Add positional arguments
        structlog.processors.StackInfoRenderer(),  # Add stack information
        structlog.stdlib.ExtraAdder(),  # Add extra attributes
        remove_color_message,  # Drop color message
        timestamper,  # Add timestamps
    ]

    if settings.debug:
        # Format the exception only in production
        # (we want to pretty-print them when using the ConsoleRenderer in development)
        shared_processors.append(structlog.processors.format_exc_info)

    # Define custom logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structlog": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    # Remove _record & _from_structlog.
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    get_renderer(),
                ],
                "foreign_pre_chain": shared_processors,
            },
        },
        "handlers": {
            "default": {
                "class": StreamHandler,
                "level": log_level,
                "formatter": "structlog",
            },
        },
        "loggers": {
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
            "uvicorn.asgi": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "fastapi": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
        },
    }

    # Configure logging using custom configuration
    dictConfig(logging_config)

    structlog_processors = [
        *shared_processors,
        # Prepare event dict for `ProcessorFormatter`.
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure(
        processors=structlog_processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
