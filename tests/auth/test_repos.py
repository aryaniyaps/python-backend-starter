from datetime import datetime
import pytest
from app.auth.repos import AuthRepo
from app.core.redis_client import redis_client
from app.core.errors import UnauthenticatedError
from app.users.models import User


@pytest.mark.asyncio
async def test_create_authentication_token() -> None:
    # Perform token creation
    user = User(
        id=1,
        username="test_user",
        email="test@example.com",
        password="hashed_password",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    token = await AuthRepo.create_authentication_token(user)

    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_verify_authentication_token_valid() -> None:
    # Create a test user and token
    user = User(
        id=1,
        username="test_user",
        email="test@example.com",
        password="hashed_password",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    token = await AuthRepo.create_authentication_token(user)

    # Perform token verification
    user_id = await AuthRepo.verify_authentication_token(token)

    assert user_id == 1


@pytest.mark.asyncio
async def test_verify_authentication_token_invalid() -> None:
    # Perform token verification for an invalid token
    with pytest.raises(UnauthenticatedError):
        await AuthRepo.verify_authentication_token("invalid_token")


@pytest.mark.asyncio
async def test_remove_authentication_token() -> None:
    # Create a test user and token
    user = User(
        id=1,
        username="test_user",
        email="test@example.com",
        password="hashed_password",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    token = await AuthRepo.create_authentication_token(user)

    # Perform token removal
    await AuthRepo.remove_authentication_token(token)

    # Verify that the token is no longer in Redis
    assert (
        await redis_client.get(
            AuthRepo.generate_authentication_token_key(token),
        )
        is None
    )
