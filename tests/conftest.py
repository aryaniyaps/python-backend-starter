from contextlib import aclosing, asynccontextmanager
from typing import AsyncIterator, Iterator

import pytest
from aioinject import Container, InjectionContext, providers
from alembic import command
from alembic.config import Config
from falcon.asgi import App
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncConnection

from app import create_app
from app.auth.repos import AuthRepo
from app.auth.services import AuthService
from app.core.containers import container
from app.core.database import engine
from app.users.models import User
from app.users.repos import UserRepo
from app.users.services import UserService

pytest_plugins = [
    "anyio",
]


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Get the anyio backend"""
    return "asyncio"


@pytest.fixture(scope="session")
def app() -> App:
    """Initialize the app for testing."""
    return create_app(testing=True)


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


@pytest.fixture
async def redis_client(injection_context: InjectionContext) -> Redis:
    """Get the redis client."""
    return await injection_context.resolve(Redis)


@pytest.fixture
async def auth_repo(injection_context: InjectionContext) -> AuthRepo:
    """Get the authentication repository."""
    return await injection_context.resolve(AuthRepo)


@pytest.fixture
async def user_repo(injection_context: InjectionContext) -> UserRepo:
    """Get the user repository."""
    return await injection_context.resolve(UserRepo)


@pytest.fixture
async def auth_service(injection_context: InjectionContext) -> AuthService:
    """Get the authentication service."""
    return await injection_context.resolve(AuthService)


@pytest.fixture
async def user_service(injection_context: InjectionContext) -> UserService:
    """Get the user service."""
    return await injection_context.resolve(UserService)


@asynccontextmanager
async def test_database_connection() -> AsyncIterator[AsyncConnection]:
    """Get the test database connection."""
    async with engine.begin() as connection:
        transaction = await connection.begin_nested()
        # yield database connection
        yield connection
        if transaction.is_active:
            await transaction.rollback()
        await connection.rollback()


@pytest.fixture(scope="session")
async def test_container() -> AsyncIterator[Container]:
    """Initialize the container for testing."""
    async with aclosing(container):
        with container.override(
            provider=providers.Callable(
                test_database_connection,
            ),
        ):
            yield container


@pytest.fixture(autouse=True)
async def injection_context(
    test_container: Container,
) -> AsyncIterator[InjectionContext]:
    """Get the injection context."""
    async with test_container.context() as context:
        yield context
