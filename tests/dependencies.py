from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncConnection

from app.core.database import database_engine


async def get_test_database_connection() -> AsyncGenerator[AsyncConnection, None]:
    """Get the test database connection."""
    async with database_engine.connect() as connection:
        async with connection.begin() as transaction:
            try:
                # yield database connection
                yield connection
            finally:
                print("ROLLING BACK TRANSACTION")
                await transaction.rollback()
