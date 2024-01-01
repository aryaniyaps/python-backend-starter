import pytest
from argon2 import PasswordHasher
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repos import AuthRepo
from app.users.repos import UserRepo


@pytest.fixture
def auth_repo(
    database_session: AsyncSession,
    redis_client: Redis,
) -> AuthRepo:
    """Get the authentication repository."""
    return AuthRepo(
        session=database_session,
        redis_client=redis_client,
    )


@pytest.fixture
def user_repo(
    database_session: AsyncSession,
    password_hasher: PasswordHasher,
) -> UserRepo:
    """Get the user repository."""
    return UserRepo(
        session=database_session,
        password_hasher=password_hasher,
    )
