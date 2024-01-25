from collections.abc import Awaitable, Callable

import structlog
from asgi_correlation_id.context import correlation_id
from fastapi import Request, Response


async def logging_middleware(
    request: Request,
    call_next: Callable[
        [Request],
        Awaitable[Response],
    ],
) -> Response:
    """Set structlog context variables for the request."""
    request_id = correlation_id.get()

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
    )

    response: Response = await call_next(request)

    return response
