from datetime import timedelta

import pytest

from app.auth.models import PasswordResetToken
from app.auth.repos import AuthRepo
from app.core.constants import PASSWORD_RESET_TOKEN_EXPIRES_IN
from app.core.errors import UnauthenticatedError
from app.core.redis_client import redis_client
from app.users.models import User

pytestmark = pytest.mark.asyncio


async def test_create_authentication_token(user: User) -> None:
    """Ensure we can create an authentication token."""
    token = await AuthRepo.create_authentication_token(user)

    assert isinstance(token, str)


async def test_verify_authentication_token_valid(user: User) -> None:
    """Ensure we can verify an authentication token."""
    token = await AuthRepo.create_authentication_token(user)

    # Perform token verification
    user_id = await AuthRepo.verify_authentication_token(token)

    assert user_id == user.id


async def test_verify_authentication_token_invalid() -> None:
    """Ensure verifying an invalid token raises an error."""
    with pytest.raises(UnauthenticatedError):
        await AuthRepo.verify_authentication_token("invalid_token")


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


async def test_create_password_reset_token(user: User) -> None:
    """Ensure a password reset token is created."""

    reset_token = await AuthRepo.create_password_reset_token(user_id=user.id)

    assert isinstance(reset_token, PasswordResetToken)
    assert reset_token.user_id == user.id
    assert reset_token.token
    assert reset_token.expires_at - reset_token.created_at == timedelta(
        seconds=PASSWORD_RESET_TOKEN_EXPIRES_IN,
    )


async def test_get_password_reset_token(user: User) -> None:
    """Ensure getting a password reset token works."""
    reset_token = await AuthRepo.create_password_reset_token(user_id=user.id)

    retrieved_reset_token = await AuthRepo.get_password_reset_token(
        password_reset_token=reset_token.token,
    )

    assert isinstance(reset_token, PasswordResetToken)
    assert reset_token == retrieved_reset_token


async def test_get_password_reset_token_not_found() -> None:
    """Ensure getting a non-existent password reset token returns None."""

    reset_token = await AuthRepo.get_password_reset_token(
        password_reset_token="nonexistent_token",
    )

    assert reset_token is None
