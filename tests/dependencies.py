from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncConnection

from app.core.database import database_engine


async def get_test_database_connection() -> AsyncGenerator[AsyncConnection, None]:
    """Get the test database connection."""
    async with database_engine.begin() as connection:
        transaction = await connection.begin_nested()
        # yield database connection
        yield connection
        if transaction.is_active:
            await transaction.rollback()
        await connection.rollback()
