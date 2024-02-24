from fastapi import Request
from limits import RateLimitItem, parse

from app.lib.errors import RateLimitExceededError
from app.lib.rate_limiter import (
    get_path_identifier,
    get_request_identifier,
    rate_limiter,
)


class RateLimiter:
    """
    Rate limiter dependency.

    Performs secondary (route-specific) rate limiting.
    """

    rate_limit: RateLimitItem

    def __init__(self, limit: str) -> None:
        self.rate_limit = parse(limit)

    def __call__(self, request: Request) -> None:
        request_identifier = get_request_identifier(request)
        path_identifier = get_path_identifier(request)

        # set rate limit stats on the request's state.
        # this is used by the rate limiter middleware to
        # set metadata on the response headers.
        request.state.secondary_rate_limit_window_stats = rate_limiter.get_window_stats(
            self.rate_limit,
            request_identifier,
            path_identifier,
        )

        # perform secondary rate limiting
        if not rate_limiter.hit(
            self.rate_limit,
            request_identifier,
            path_identifier,
        ):
            raise RateLimitExceededError(
                message="You are being rate limited.",
                is_primary=False,
            )
