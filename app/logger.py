from logging import StreamHandler
from logging.config import dictConfig

import structlog
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer
from structlog.types import Processor

from app.config import settings


def get_renderer() -> JSONRenderer | ConsoleRenderer:
    """Get the logging renderer."""
    if settings.debug:
        return ConsoleRenderer()
    return JSONRenderer(indent=1, sort_keys=True)


def setup_logging(log_level: str) -> None:
    """Set up application logging."""
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,  # Merge context variables
        structlog.stdlib.add_log_level,  # Add log level
        structlog.stdlib.PositionalArgumentsFormatter(),  # Add positional arguments
        structlog.processors.TimeStamper(fmt="iso", utc=True),  # Add timestamps
        structlog.stdlib.ExtraAdder(),  # Add extra attributes
        structlog.processors.StackInfoRenderer(),  # Add stack information
    ]

    if settings.debug:
        # Format the exception only in production
        # (we want to pretty-print them when using the ConsoleRenderer in development)
        shared_processors.append(structlog.processors.format_exc_info)

    structlog_processors = [
        structlog.stdlib.filter_by_level,  # Filter out log levels
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
                "formatter": "structlog",
                "class": StreamHandler,
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
            "fastapi": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
        },
    }

    # Configure logging using custom configuration
    dictConfig(logging_config)
