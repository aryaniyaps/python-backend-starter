from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from app.config import settings

database_engine = create_async_engine(
    url=str(settings.database_url),
    echo=settings.debug,
    pool_size=settings.database_pool_size,
    max_overflow=0,
    pool_recycle=3600,
    pool_use_lifo=True,
    pool_pre_ping=True,
)


async def get_database_connection() -> AsyncGenerator[AsyncConnection, None]:
    """Get the database connection."""
    async with database_engine.begin() as connection:
        yield connection


database_metadata = MetaData(
    naming_convention={
        "ix": "%(column_0_label)s_idx",
        "uq": "%(table_name)s_%(column_0_name)s_key",
        "ck": "%(table_name)s_%(constraint_name)s_check",
        "fk": "%(table_name)s_%(column_0_name)s_fkey",
        "pk": "%(table_name)s_pkey",
    }
)
