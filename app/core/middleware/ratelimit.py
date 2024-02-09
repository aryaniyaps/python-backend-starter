from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from limits import parse

from app.core.errors import RateLimitExceededError
from app.core.ratelimiter import rate_limiter

# ideal workflow: all ratelimiting must be done from the middleware
# first check if ratelimiting is exempted for the route/operation
# second, enforce global ratelimit
# third, enforce route/operation-specific ratelimit
# we want some way via which we can get the route-specific limit and exempt metadata here.
# maybe add a marker on the routes?
# or have a separate dict based config based on URLs?
# like:
# limit_rules = {
#     "/auth/login": "50/hour",
# }

primary_rate_limit = "5000/hour"

secondary_rate_limits = {
    "POST-/auth/register": "15/hour",
    "POST-/auth/sessions": "",
}

exempted_routes = [
    "/health",
]


def _get_request_identifier(request: Request) -> str:
    """Get the unique identifier for the request."""
    return request.client.host


def _get_path_identifier(request: Request) -> str:
    """Get the unique identifier for the path operation."""
    return f"{request.method}-{request.url.path}"


def _get_secondary_ratelimit(request: Request) -> str:
    """Get the secondary ratelimit for the request."""
    secondary_ratelimit = secondary_rate_limits.get(_get_path_identifier(request), None)
    if secondary_ratelimit is not None:
        return secondary_ratelimit
    # default secondary ratelimit
    return "100/hour"


async def ratelimit_middleware(
    request: Request,
    call_next: Callable[
        [Request],
        Awaitable[Response],
    ],
) -> Response:
    """Enforce ratelimiting for the request."""
    if request.url in exempted_routes:
        # exempt route from ratelimiting
        response = await call_next(request)

    # perform primary ratelimiting
    if not rate_limiter.hit(
        parse(primary_rate_limit),
        _get_request_identifier(request),
    ):
        raise RateLimitExceededError(
            message="You are being ratelimited.",
        )

    # perform secondary ratelimiting
    if not rate_limiter.hit(
        parse(_get_secondary_ratelimit(request)),
        _get_request_identifier(request),
        _get_path_identifier(request),
    ):
        raise RateLimitExceededError(
            message="You are being ratelimited.",
        )

    response = await call_next(request)

    primary_window_stats = rate_limiter.get_window_stats(
        parse(primary_rate_limit),
        _get_request_identifier(request),
    )

    secondary_window_stats = rate_limiter.get_window_stats(
        parse(_get_secondary_ratelimit(request)),
        _get_request_identifier(request),
        _get_path_identifier(request),
    )

    response.headers["X-Ratelimit-Primary-Remaining"] = primary_window_stats.remaining
    response.headers["X-Ratelimit-Primary-Reset"] = primary_window_stats.reset_time
    response.headers["X-Ratelimit-Secondary-Remaining"] = (
        secondary_window_stats.remaining
    )
    response.headers["X-Ratelimit-Secondary-Reset"] = secondary_window_stats.reset_time

    return response
