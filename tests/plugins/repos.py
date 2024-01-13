import pytest
from app.auth.repos import AuthRepo
from app.users.repos import UserRepo
from argon2 import PasswordHasher
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def auth_repo(
    test_database_session: AsyncSession,
    redis_client: Redis[bytes],
) -> AuthRepo:
    """Get the authentication repository."""
    return AuthRepo(
        session=test_database_session,
        redis_client=redis_client,
    )


@pytest.fixture
def user_repo(
    test_database_session: AsyncSession,
    password_hasher: PasswordHasher,
) -> UserRepo:
    """Get the user repository."""
    return UserRepo(
        session=test_database_session,
        password_hasher=password_hasher,
    )
