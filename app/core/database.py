from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from app.config import Settings


def get_database_engine(settings: Settings) -> AsyncEngine:
    """Get the database engine."""
    return create_async_engine(
        url=str(settings.database_url),
        echo=settings.debug,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,
    )


@asynccontextmanager
async def get_database_connection(
    engine: AsyncEngine,
) -> AsyncIterator[AsyncConnection]:
    """Get the database connection."""
    async with engine.begin() as connection:
        yield connection


database_metadata = MetaData()
