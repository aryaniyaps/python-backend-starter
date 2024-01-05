from typing import AsyncGenerator, Iterator

import pytest
from alembic import command
from alembic.config import Config
from argon2 import PasswordHasher
from redis.asyncio import Redis
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, async_sessionmaker

from app.auth.repos import AuthRepo
from app.core.database import database_engine
from app.core.redis_client import get_redis_client
from app.core.security import get_password_hasher
from app.users.models import User
from app.users.repos import UserRepo

pytest_plugins = [
    "anyio",
    "tests.plugins.repos",
    "tests.plugins.services",
]


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Get the anyio backend"""
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def setup_test_database() -> Iterator[None]:
    """Set up the test database."""

    alembic_cfg = Config("alembic.ini")

    # apply migrations to the test database
    command.upgrade(
        alembic_cfg,
        revision="head",
    )

    yield

    # cleanup the test database
    command.downgrade(
        alembic_cfg,
        revision="base",
    )


@pytest.fixture
async def user(user_repo: UserRepo) -> User:
    """Create an user for testing."""
    return await user_repo.create_user(
        username="tester",
        email="tester@example.org",
        password="password",
    )


@pytest.fixture
async def authentication_token(user: User, auth_repo: AuthRepo) -> str:
    """Create an authentication token for the user."""
    return await auth_repo.create_authentication_token(user_id=user.id)


@pytest.fixture(scope="session")
async def test_database_connection() -> AsyncGenerator[AsyncConnection, None]:
    """Get the test database connection."""
    async with database_engine.begin() as connection:
        yield connection


@pytest.fixture
async def database_session() -> AsyncGenerator[AsyncSession, None]:
    """Get the database session."""
    connection = await database_engine.connect()
    transaction = await connection.begin()

    test_session_maker = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=database_engine,
    )
    async_session = test_session_maker(bind=connection)
    nested = await connection.begin_nested()

    @event.listens_for(async_session.sync_session, "after_transaction_end")
    def end_savepoint(_session, _transaction) -> None:
        nonlocal nested

        if not nested.is_active and connection.sync_connection:
            nested = connection.sync_connection.begin_nested()

    yield async_session

    await transaction.rollback()
    await async_session.close()
    await connection.close()


@pytest.fixture(scope="session")
def redis_client() -> Redis:
    """Get the redis client."""
    return get_redis_client()


@pytest.fixture(scope="session")
def password_hasher() -> PasswordHasher:
    """Get the password hasher."""
    return get_password_hasher()
