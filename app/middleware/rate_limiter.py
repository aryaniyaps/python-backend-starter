from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from limits import WindowStats, parse

from app.lib.constants import PRIMARY_RATE_LIMIT
from app.lib.errors import RateLimitExceededError
from app.lib.rate_limiter import (
    get_path_identifier,
    get_request_identifier,
    rate_limiter,
)

primary_rate_limit = parse(PRIMARY_RATE_LIMIT)

# FIXME: it would be better to exempt rate limiting with a dependency
# on the endpoint instead. Trailing slashes affect ratelimiting here and
# we need to update the URLs whenever it changes somewhere else.
primary_route_exemptions = [
    "GET-/health/",
]


async def rate_limiter_middleware(
    request: Request,
    call_next: Callable[
        [Request],
        Awaitable[Response],
    ],
) -> Response:
    """
    Rate limiter middleware.

    Performs primary (API-wide) rate limiting and sets rate
    limiting metadata on the response headers.
    """
    if get_path_identifier(request) in primary_route_exemptions:
        # exempt from rate limiting
        return await call_next(request)

    if not rate_limiter.hit(
        primary_rate_limit,
        get_request_identifier(request),
    ):
        raise RateLimitExceededError(
            message="You are being rate limited.",
            is_primary=True,
        )

    response = await call_next(request)

    primary_window_stats = rate_limiter.get_window_stats(
        primary_rate_limit,
        get_request_identifier(request),
    )

    try:
        # get secondary rate limit stats if they exist
        secondary_window_stats: WindowStats | None = (
            request.state.secondary_rate_limit_window_stats
        )
    except AttributeError:
        secondary_window_stats = None

    response.headers["X-Ratelimit-Primary-Remaining"] = str(
        primary_window_stats.remaining,
    )

    response.headers["X-Ratelimit-Primary-Reset"] = str(
        primary_window_stats.reset_time,
    )

    if secondary_window_stats is not None:
        response.headers["X-Ratelimit-Secondary-Remaining"] = str(
            secondary_window_stats.remaining,
        )

        response.headers["X-Ratelimit-Secondary-Reset"] = str(
            secondary_window_stats.reset_time,
        )

    return response
