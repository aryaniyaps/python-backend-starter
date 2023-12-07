from contextlib import asynccontextmanager
from typing import AsyncGenerator

from redis.asyncio import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncConnection

from app.config import settings
from app.core.database import engine
from app.core.dependency_container import DependencyContainer


@asynccontextmanager
async def get_database_connection() -> AsyncGenerator[AsyncConnection, None]:
    """Get a database connection."""
    async with engine.connect() as connection:
        yield connection


def get_redis_client() -> Redis:
    """Get the redis client."""
    return from_url(
        url=str(settings.redis_url),
    )


def register_dependencies(container: DependencyContainer) -> None:
    """Register dependencies for the container."""
    container.register(
        AsyncConnection,
        get_database_connection,
    )
    # we need only one redis client instance
    # per application (singleton)
    container.register(
        Redis,
        get_redis_client(),
    )


def create_container() -> DependencyContainer:
    """Initialize a container."""
    container = DependencyContainer()
    register_dependencies(container)
    return container


container = create_container()
