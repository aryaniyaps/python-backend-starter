from fastapi import Request
from limits.storage import RedisStorage
from limits.strategies import MovingWindowRateLimiter

from app.config import settings

rate_limiter = MovingWindowRateLimiter(
    storage=RedisStorage(uri=str(settings.redis_url)),
)


def get_request_identifier(request: Request) -> str:
    """Get the unique identifier for the request."""
    return request.client.host


def get_path_identifier(request: Request) -> str:
    """Get the unique identifier for the path operation."""
    return f"{request.method}-{request.url.path}"
