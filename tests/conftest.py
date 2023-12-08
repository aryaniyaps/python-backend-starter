from asyncio import AbstractEventLoop, get_event_loop
from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterator

import pytest
from aioinject import providers
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

# the default `event_loop` fixture is function scoped,
# which means we cannot use it for async session scoped
# fixtures out of the box


@pytest.fixture(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    """Get the event loop."""
    loop = get_event_loop()
    yield loop
    if loop.is_running:
        loop.close()


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


@pytest.fixture(scope="session")
async def user(user_repo: UserRepo) -> User:
    """Create an user for testing."""
    return await user_repo.create_user(
        username="tester",
        email="tester@example.org",
        password="password",
    )


@pytest.fixture(scope="session")
async def authentication_token(user: User, auth_repo: AuthRepo) -> str:
    """Create an authentication token for the user."""
    return await auth_repo.create_authentication_token(user_id=user.id)


@pytest.fixture(scope="session")
async def connection() -> AsyncIterator[AsyncConnection]:
    """Get the database connection."""
    async with container.context() as context:
        yield await context.resolve(AsyncConnection)


@pytest.fixture(scope="session")
def redis_client() -> Iterator[Redis]:
    """Get the redis client."""
    with container.sync_context() as context:
        yield context.resolve(Redis)


@pytest.fixture(scope="session")
def auth_repo(connection: AsyncConnection, redis_client: Redis) -> AuthRepo:
    """Get the authentication repository."""
    return AuthRepo(
        connection=connection,
        redis_client=redis_client,
    )


@pytest.fixture(scope="session")
def user_repo(connection: AsyncConnection) -> UserRepo:
    """Get the user repository."""
    return UserRepo(
        connection=connection,
    )


@pytest.fixture(scope="session")
def auth_service(auth_repo: AuthRepo, user_repo: UserRepo) -> AuthService:
    """Get the authentication service."""
    return AuthService(
        auth_repo=auth_repo,
        user_repo=user_repo,
    )


@pytest.fixture(scope="session")
def user_service(user_repo: UserRepo) -> UserService:
    """Get the user service."""
    return UserService(
        user_repo=user_repo,
    )


@asynccontextmanager
async def get_test_database_connection() -> AsyncIterator[AsyncConnection]:
    """
    Get a database conenction with a transaction
    setup inside for each test case.
    """
    async with engine.connect() as connection:
        # begin database transaction
        transaction = await connection.begin()

        yield connection

        # rollback database transaction
        await transaction.rollback()


@pytest.fixture(scope="session")
def setup_test_container() -> Iterator[None]:
    """Setup the container for testing."""
    with container.override(
        provider=providers.Callable(
            get_test_database_connection,
        ),
    ):
        yield
