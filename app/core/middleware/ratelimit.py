from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from limits import WindowStats


async def ratelimit_middleware(
    request: Request,
    call_next: Callable[
        [Request],
        Awaitable[Response],
    ],
) -> Response:
    """Set ratelimit headers for the request."""
    response = await call_next(request)

    # Add rate limit headers if they are available in the request state
    if "ratelimit_window_stats" in request.state:
        window_stats: WindowStats = request.state["ratelimit_window_stats"]
        response.headers["X-Ratelimit-Remaining"] = window_stats.remaining
        response.headers["X-Ratelimit-Reset"] = window_stats.reset_time

    return response
