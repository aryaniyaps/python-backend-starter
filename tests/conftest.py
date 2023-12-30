from contextlib import asynccontextmanager
from typing import AsyncGenerator, Iterator

import pytest
from alembic import command
from alembic.config import Config
from argon2 import PasswordHasher
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncConnection

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


@asynccontextmanager
async def get_test_database_connection() -> AsyncGenerator[AsyncConnection, None]:
    """Get the test database connection."""
    async with database_engine.begin() as connection:
        transaction = await connection.begin_nested()
        # yield database connection
        yield connection
        if transaction.is_active:
            await transaction.rollback()
        await connection.rollback()


@pytest.fixture
async def database_connection() -> AsyncGenerator[AsyncConnection, None]:
    """Get the database connection."""
    async with get_test_database_connection() as connection:
        yield connection


@pytest.fixture(scope="session")
def redis_client() -> Redis:
    """Get the redis client."""
    return get_redis_client()


@pytest.fixture(scope="session")
def password_hasher() -> PasswordHasher:
    """Get the password hasher."""
    return get_password_hasher()
