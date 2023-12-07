from asyncio import AbstractEventLoop, get_event_loop
from typing import AsyncIterator, Iterator

import pytest
from alembic import command
from alembic.config import Config
from falcon.asgi import App
from sqlalchemy.ext.asyncio import AsyncConnection

from app import create_app
from app.core.database import engine
from app.users.models import User
from app.users.repos import UserRepo


@pytest.fixture(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    """
    Get the event loop (Overwriting the existing
    fixture to give it a session scope, for use with
    session-scoped fixtures).
    """
    loop = get_event_loop()
    yield loop
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


@pytest.fixture(autouse=True)
async def test_connection() -> AsyncIterator[AsyncConnection]:
    """Set up a transaction inside a database
    connection for each test case."""
    async with engine.connect() as connection:
        # begin database transaction.
        transaction = await connection.begin()

        yield connection

        # rollback database transaction.
        await transaction.rollback()


@pytest.fixture(scope="session")
async def user() -> User:
    """Create an user for testing."""
    return await UserRepo.create_user(
        username="tester",
        email="tester@example.org",
        password="password",
    )
