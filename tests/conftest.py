from typing import AsyncGenerator, Iterator

import pytest
from alembic import command
from alembic.config import Config
from argon2 import PasswordHasher
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from app.auth.repos import AuthRepo
from app.config import Settings, get_settings
from app.core.database import get_database_engine
from app.core.redis_client import get_redis_client
from app.core.security import get_password_hasher
from app.users.models import User
from app.users.repos import UserRepo
from tests.dependencies import get_test_database_connection

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


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Setup the settings for testing."""
    return get_settings()


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
def database_engine(test_settings: Settings) -> AsyncEngine:
    """Get the database engine."""
    return get_database_engine(settings=test_settings)


@pytest.fixture
async def database_connection(
    database_engine: AsyncEngine,
) -> AsyncGenerator[AsyncConnection, None]:
    """Get the database connection."""
    async with get_test_database_connection(
        engine=database_engine,
    ) as connection:
        yield connection


@pytest.fixture(scope="session")
async def redis_client(test_settings: Settings) -> AsyncGenerator[Redis, None]:
    """Get the redis client."""
    async with get_redis_client(settings=test_settings) as redis_client:
        yield redis_client


@pytest.fixture(scope="session")
def password_hasher() -> PasswordHasher:
    """Get the password hasher."""
    return get_password_hasher()
