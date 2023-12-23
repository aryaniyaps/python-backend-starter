from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from app.config import Settings


def get_database_engine(settings: Settings) -> AsyncEngine:
    """Get the database engine."""
    return create_async_engine(
        url=str(settings.database_url),
        echo=settings.debug,
        pool_size=settings.database_pool_size,
        pool_pre_ping=True,
    )


@asynccontextmanager
async def get_database_connection(
    engine: Annotated[
        AsyncEngine,
        Depends(
            dependency=get_database_engine,
        ),
    ],
) -> AsyncGenerator[AsyncConnection, None]:
    """Get the database connection."""
    async with engine.begin() as connection:
        yield connection


database_metadata = MetaData()
