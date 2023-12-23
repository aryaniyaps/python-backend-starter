from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterator

import pytest
from alembic import command
from alembic.config import Config
from argon2 import PasswordHasher
from di import Container, bind_by_type
from di.dependent import Dependent
from redis.asyncio import Redis
from sanic import Sanic
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from app import create_app
from app.auth.repos import AuthRepo
from app.config import Settings
from app.core.containers import DIScope, create_container
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


@pytest.fixture(scope="session")
async def app(
    test_container: Container,
    test_settings: Settings,
) -> AsyncIterator[Sanic]:
    """Initialize the app for testing."""
    async with test_container.enter_scope(DIScope.APP) as app_state:
        yield create_app(
            settings=test_settings,
            container=test_container,
            app_state=app_state,
        )


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


@asynccontextmanager
async def get_test_database_connection(
    engine: AsyncEngine,
) -> AsyncIterator[AsyncConnection]:
    """Get the test database connection."""
    async with engine.begin() as connection:
        transaction = await connection.begin_nested()
        # yield database connection
        yield connection
        if transaction.is_active:
            await transaction.rollback()
        await connection.rollback()


@pytest.fixture(scope="session")
def test_container() -> Container:
    """Setup the container for testing."""
    container = create_container()
    container.bind(
        bind_by_type(
            Dependent(
                get_test_database_connection,
                scope=DIScope.REQUEST,
            ),
            AsyncConnection,
        )
    )
    return container


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Setup the settings for testing."""
    return Settings()  # type: ignore


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
async def redis_client(test_settings: Settings) -> AsyncIterator[Redis]:
    """Get the redis client."""
    async with get_redis_client(settings=test_settings) as redis_client:
        yield redis_client


@pytest.fixture(scope="session")
def password_hasher() -> PasswordHasher:
    """Get the password hasher."""
    return get_password_hasher()
