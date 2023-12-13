from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterator

import inject
import pytest
from alembic import command
from alembic.config import Config
from falcon.asgi import App
from inject import Binder
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncConnection

from app import create_app
from app.auth.repos import AuthRepo
from app.core.containers import app_config
from app.core.database import engine
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
def app() -> App:
    """Initialize the app for testing."""
    return create_app()


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
async def get_test_database_connection() -> AsyncIterator[AsyncConnection]:
    """Get the test database connection."""
    async with engine.begin() as connection:
        transaction = await connection.begin_nested()
        # yield database connection
        yield connection
        if transaction.is_active:
            await transaction.rollback()
        await connection.rollback()


def tests_config(binder: Binder) -> None:
    """Configure dependencies for the test environment."""
    # reuse existing configuration
    binder.install(app_config)

    # override dependencies
    binder.bind_to_provider(
        AsyncConnection,
        get_test_database_connection,
    )


@pytest.fixture(scope="session", autouse=True)
def setup_test_dependencies() -> None:
    """Setup dependencies for testing."""
    inject.clear_and_configure(
        tests_config,
        allow_override=True,  # type: ignore
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
def redis_client() -> Redis:
    """Get the redis client."""
    return inject.instance(Redis)
