from functools import lru_cache

from redis.asyncio import Redis

from app.config import settings


@lru_cache
def get_redis_client() -> Redis[bytes]:
    """Get the redis client."""
    return Redis.from_url(
        url=str(settings.redis_url),
    )
