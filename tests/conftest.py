from typing import AsyncIterator

import pytest
from alembic.command import stamp
from alembic.config import Config
from falcon.asgi import App
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from app import create_app
from app.core.database import database_metadata, engine
from app.core.security import password_hasher
from app.users.models import User
from app.users.repos import UserRepo


@pytest.fixture(scope="session")
def app() -> App:
    """Initialize the app for testing."""
    return create_app()


@pytest.fixture(scope="session")
async def db_engine() -> AsyncIterator[AsyncEngine]:
    """
    Set up the database engine.

    :return: The test database engine.
    """
    alembic_cfg = Config("alembic.ini")
    async with engine.begin() as conn:
        # create database tables.
        await conn.run_sync(database_metadata.create_all)

    # stamp the revisions table.
    stamp(alembic_cfg, revision="head")

    # yield database engine.
    yield engine

    async with engine.begin() as conn:
        # drop database tables.
        await conn.run_sync(database_metadata.drop_all)

    # stamp the revisions table.
    stamp(alembic_cfg, revision=None, purge=True)


@pytest.fixture(autouse=True)
async def setup_transaction(db_engine: AsyncEngine) -> AsyncIterator[AsyncConnection]:
    """Set up a transaction inside a database
    connection for each test case."""
    async with db_engine.connect() as connection:
        # begin database transaction.
        transaction = await connection.begin()
        # yield connection with transaction.
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
