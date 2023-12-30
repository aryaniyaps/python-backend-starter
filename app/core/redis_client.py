from redis.asyncio import ConnectionPool, Redis

from app.config import settings

connection_pool = ConnectionPool.from_url(
    url=str(settings.redis_url),
)


def get_redis_client() -> Redis:
    """Get the redis client."""
    return Redis.from_pool(
        connection_pool=connection_pool,
    )
