from fastapi import Request
from limits import parse
from limits.storage import RedisStorage
from limits.strategies import MovingWindowRateLimiter

from app.config import settings
from app.core.errors import RateLimitExceededError

rate_limiter = MovingWindowRateLimiter(
    storage=RedisStorage(uri=settings.redis_url),
)


class RateLimiter:
    def __init__(self, limit: str, cost: int = 1) -> None:
        self._rate_limit = parse(limit)
        self._cost = cost

    def _get_request_identifier(self, request: Request) -> str:
        """Get the unique identifier for the request."""
        return request.client.host

    def _get_path_identifier(self, request: Request) -> str:
        """Get the unique identifier for the path operation."""
        return f"{request.method}/{request.url.path}"

    def __call__(self, request: Request) -> None:
        request.state["ratelimit_window_stats"] = rate_limiter.get_window_stats(
            self._rate_limit,
            self._get_request_identifier(
                request=request,
            ),
            self._get_path_identifier(
                request=request,
            ),
        )
        if not rate_limiter.hit(
            self._rate_limit,
            self._get_request_identifier(
                request=request,
            ),
            self._get_path_identifier(
                request=request,
            ),
            cost=self._cost,
        ):
            raise RateLimitExceededError
