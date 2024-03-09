from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.database.session_factory import async_session_factory


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """Get the database session."""
    async with async_session_factory() as session:
        yield session
