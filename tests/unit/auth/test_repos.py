import pytest
from app.auth.repos import AuthRepo
from app.core.redis_client import redis_client
from app.core.errors import UnauthenticatedError
from app.users.models import User


@pytest.mark.asyncio
async def test_create_authentication_token(user: User) -> None:
    """Ensure we can create an authentication token."""
    token = await AuthRepo.create_authentication_token(user)

    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_verify_authentication_token_valid(user: User) -> None:
    """Ensure we can verify an authentication token."""
    token = await AuthRepo.create_authentication_token(user)

    # Perform token verification
    user_id = await AuthRepo.verify_authentication_token(token)

    assert user_id == user.id


@pytest.mark.asyncio
async def test_verify_authentication_token_invalid() -> None:
    """Ensure verifying an invalid token raises an error."""
    with pytest.raises(UnauthenticatedError):
        await AuthRepo.verify_authentication_token("invalid_token")


@pytest.mark.asyncio
async def test_remove_authentication_token(user: User) -> None:
    """Ensure we can remove an authentication token."""
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
