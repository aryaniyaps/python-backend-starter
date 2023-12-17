from contextlib import asynccontextmanager
from typing import AsyncIterator

from redis.asyncio import Redis, from_url

from app.config import Settings


@asynccontextmanager
async def get_redis_client(settings: Settings) -> AsyncIterator[Redis]:
    """Get the redis client."""
    redis_client = from_url(
        url=str(settings.redis_url),
    )
    yield redis_client

    await redis_client.aclose()
