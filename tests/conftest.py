from collections.abc import AsyncGenerator, AsyncIterator, Iterator

import pytest
from alembic import command
from alembic.config import Config
from app.auth.repos import AuthRepo
from app.config import settings
from app.core.redis_client import get_redis_client
from app.core.security import get_password_hasher
from app.users.models import User
from app.users.repos import UserRepo
from argon2 import PasswordHasher
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

pytest_plugins = [
    "anyio",
    "tests.plugins.repos",
    "tests.plugins.services",
]


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Get the anyio backend."""
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def _setup_test_database() -> Iterator[None]:
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


@pytest.fixture(scope="session")
async def test_database_engine() -> AsyncIterator[AsyncEngine]:
    """Get the test database engine."""
    engine = create_async_engine(
        url=str(settings.database_url),
        echo=True,
        pool_use_lifo=True,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
def test_sessionmaker(
    test_database_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """Get the test session maker."""
    return async_sessionmaker(
        autoflush=False,
        expire_on_commit=False,
        bind=test_database_engine,
    )


@pytest.fixture
async def test_database_session(
    test_database_engine: AsyncEngine,
    test_sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """Get the test database session."""
    async with test_database_engine.connect() as conn:
        transaction = await conn.begin()
        test_sessionmaker.configure(bind=conn)

        async with test_sessionmaker() as session:
            yield session

        if transaction.is_active:
            await transaction.rollback()


@pytest.fixture
def redis_client() -> Redis:
    """Get the redis client."""
    return get_redis_client()


@pytest.fixture(scope="session")
def password_hasher() -> PasswordHasher:
    """Get the password hasher."""
    return get_password_hasher()
