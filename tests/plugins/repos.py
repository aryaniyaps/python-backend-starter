import pytest
from argon2 import PasswordHasher
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncConnection

from app.auth.repos import AuthRepo
from app.users.repos import UserRepo


@pytest.fixture
def auth_repo(
    database_connection: AsyncConnection,
    redis_client: Redis,
) -> AuthRepo:
    """Get the authentication repository."""
    return AuthRepo(
        connection=database_connection,
        redis_client=redis_client,
    )


@pytest.fixture
def user_repo(
    database_connection: AsyncConnection,
    password_hasher: PasswordHasher,
) -> UserRepo:
    """Get the user repository."""
    return UserRepo(
        connection=database_connection,
        password_hasher=password_hasher,
    )
