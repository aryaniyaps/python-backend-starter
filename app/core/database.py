from datetime import datetime
from typing import AsyncGenerator
from uuid import UUID

from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, registry

from app.config import settings

database_engine = create_async_engine(
    url=str(settings.database_url),
    echo=settings.debug,
    pool_size=settings.database_pool_size,
    pool_use_lifo=True,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    bind=database_engine,
    expire_on_commit=False,
)

database_metadata = MetaData(
    naming_convention={
        "ix": "%(column_0_label)s_idx",
        "uq": "%(table_name)s_%(column_0_name)s_key",
        "ck": "%(table_name)s_%(constraint_name)s_check",
        "fk": "%(table_name)s_%(column_0_name)s_fkey",
        "pk": "%(table_name)s_pkey",
    }
)


class Base(AsyncAttrs, DeclarativeBase):
    metadata = database_metadata

    registry = registry(
        type_annotation_map={
            datetime: TIMESTAMP(
                timezone=True,
            ),
            UUID: UUIDColumn(
                as_uuid=True,
            ),
        },
    )


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """Get the database session."""
    async with async_session_factory() as session:
        yield session
