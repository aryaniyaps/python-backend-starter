from typing import Annotated, AsyncGenerator

from fastapi import Depends
from redis.asyncio import Redis, from_url

from app.config import Settings, get_settings


async def get_redis_client(
    settings: Annotated[
        Settings,
        Depends(
            dependency=get_settings,
        ),
    ]
) -> AsyncGenerator[Redis, None]:
    """Get the redis client."""
    redis_client = from_url(
        url=str(settings.redis_url),
    )
    yield redis_client

    await redis_client.aclose()
