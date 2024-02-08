from http import HTTPStatus

from fastapi import HTTPException, Request
from limits import parse
from limits.storage import RedisStorage
from limits.strategies import MovingWindowRateLimiter

from app.config import settings

rate_limiter = MovingWindowRateLimiter(
    storage=RedisStorage(uri=settings.redis_url),
)


class RateLimiter:
    def __init__(self, limit: str, cost: int = 1) -> None:
        self._rate_limit = parse(limit)
        self._cost = cost

    def _get_request_identifier(self, request: Request) -> str:
        return request.client.host

    def _get_path_identifier(self, request: Request) -> str:
        return request.url.path

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
            raise HTTPException(
                status_code=HTTPStatus.TOO_MANY_REQUESTS,
                detail={
                    "message": "You are being ratelimited",
                },
            )
