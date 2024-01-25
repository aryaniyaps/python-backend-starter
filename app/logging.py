import logging
import sys
from typing import TracebackType

import structlog
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer
from structlog.types import EventDict, Processor, WrappedLogger

from app.config import settings


def get_renderer() -> JSONRenderer | ConsoleRenderer:
    """Get the logging renderer."""
    if settings.debug:
        return ConsoleRenderer()
    return JSONRenderer()


def drop_color_message_key(
    _logger: WrappedLogger,
    _name: str,
    event_dict: EventDict,
) -> EventDict:
    """
    Drop the color message from the event dict if it exists.

    Uvicorn logs the message a second time in the extra `color_message`, but we don't
    need it. This processor drops the key from the event dict if it exists.
    """
    event_dict.pop("color_message", None)
    return event_dict


def setup_logging(json_logs: bool = False, log_level: str = "INFO") -> None:
    """Set up application logging."""
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors: list[Processor] = [
        timestamper,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ExtraAdder(),
        drop_color_message_key,
        structlog.processors.StackInfoRenderer(),
    ]

    if json_logs:
        # Format the exception only for JSON logs
        # (we want to pretty-print them when using the ConsoleRenderer)
        shared_processors.append(structlog.processors.format_exc_info)

    structlog_processors = [
        *shared_processors,
        # Prepare event dict for `ProcessorFormatter`.
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure(
        processors=structlog_processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        # These run ONLY on `logging` entries that do NOT originate within
        # structlog.
        foreign_pre_chain=shared_processors,
        # These run on ALL entries after the pre_chain is done.
        processors=[
            # Remove _record & _from_structlog.
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            get_renderer(),
        ],
    )

    handler = logging.StreamHandler()
    # Use OUR `ProcessorFormatter` to format all `logging` entries.
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level.upper())

    for _log in ["uvicorn", "uvicorn.error"]:
        # Clear the log handlers for uvicorn loggers, and enable propagation
        # so the messages are caught by our root logger and formatted correctly
        # by structlog
        logging.getLogger(_log).handlers.clear()
        logging.getLogger(_log).propagate = True

    # Since we re-create the access logs ourselves, to add all information
    # in the structured log (see the `logging_middleware` in main.py), we clear
    # the handlers and prevent the logs to propagate to a logger higher up in the
    # hierarchy (effectively rendering them silent).
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = False

    def handle_exception(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> None:
        """Log uncaught exceptions except for keyboard interrupt errors."""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        root_logger.error(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exception
