from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from app.core.database import get_database_engine


@asynccontextmanager
async def get_test_database_connection(
    engine: Annotated[
        AsyncEngine,
        Depends(
            dependency=get_database_engine,
        ),
    ],
) -> AsyncGenerator[AsyncConnection, None]:
    """Get the test database connection."""
    async with engine.begin() as connection:
        transaction = await connection.begin_nested()
        # yield database connection
        yield connection
        if transaction.is_active:
            await transaction.rollback()
        await connection.rollback()
