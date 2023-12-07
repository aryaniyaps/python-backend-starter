from asyncio import AbstractEventLoop, get_event_loop
from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterator

import pytest
from aioinject import providers
from alembic import command
from alembic.config import Config
from falcon.asgi import App
from sqlalchemy.ext.asyncio import AsyncConnection

from app import create_app
from app.core.containers import container
from app.core.database import engine
from app.users.models import User
from app.users.repos import UserRepo


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    """Get the event loop."""
    return get_event_loop()


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
async def user() -> User:
    """Create an user for testing."""
    return await UserRepo.create_user(
        username="tester",
        email="tester@example.org",
        password="password",
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


# FIXME: the issue is, as soon as the function call gets over
# example: UserRepo.create_user, the connection dependency closes.
# thus the connection rolls back and the user is removed from the
# database. This is making tests fail.


@pytest.fixture(scope="function", autouse=True)
def setup_test_container() -> Iterator[None]:
    """Set up the container for testing."""
    with container.override(
        provider=providers.Callable(
            get_test_database_connection,
        ),
    ):
        yield
