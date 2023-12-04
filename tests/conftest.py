from typing import AsyncIterator

import pytest
from alembic import command
from alembic.config import Config
from falcon.asgi import App
from lagom import Container
from sqlalchemy.ext.asyncio import AsyncConnection

from app import create_app
from app.core.containers import container
from app.core.database import engine
from app.core.security import password_hasher
from app.users.models import User
from app.users.repos import UserRepo


@pytest.fixture(scope="session")
def app() -> App:
    """Initialize the app for testing."""
    return create_app()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database() -> AsyncIterator[None]:
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


@pytest.fixture()
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
async def user() -> AsyncIterator[User]:
    """Create an user for testing."""
    user = await UserRepo.create_user(
        username="tester",
        email="tester@example.org",
        password_hash=password_hasher.hash(
            password="password",
        ),
    )

    yield user

    await UserRepo.delete_user(user_id=user.id)
