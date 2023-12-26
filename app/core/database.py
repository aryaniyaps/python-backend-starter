from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from app.config import Settings, get_settings


def get_database_engine(
    settings: Annotated[
        Settings,
        Depends(
            dependency=get_settings,
        ),
    ]
) -> AsyncEngine:
    """Get the database engine."""
    return create_async_engine(
        url=str(settings.database_url),
        echo=settings.debug,
        pool_size=settings.database_pool_size,
        pool_pre_ping=True,
    )


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


database_metadata = MetaData(
    naming_convention={
        "ix": "%(column_0_label)s_idx",
        "uq": "%(table_name)s_%(column_0_name)s_key",
        "ck": "%(table_name)s_%(constraint_name)s_check",
        "fk": "%(table_name)s_%(column_0_name)s_fkey",
        "pk": "%(table_name)s_pkey",
    }
)
