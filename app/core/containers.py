from typing import AsyncIterator

from lagom import (
    Container,
    ContextContainer,
    context_dependency_definition,
    dependency_definition,
)
from redis.asyncio import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncConnection

from app.config import Settings
from app.core.database import engine

container = Container()


@context_dependency_definition(container=container)
async def get_database_connection() -> AsyncIterator[AsyncConnection]:
    """Get a database connection"""
    async with engine.connect() as connection:
        yield connection


@dependency_definition(container=container, singleton=True)
def get_redis_client() -> Redis:
    """Get the redis client."""
    return from_url(
        url=str(Settings.redis_url),
    )


context_container = ContextContainer(
    container=container,
    context_types=[
        AsyncConnection,
    ],
)
