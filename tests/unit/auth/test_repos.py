from datetime import timedelta
from hashlib import sha256

import pytest
from redis.asyncio import Redis

from app.auth.models import PasswordResetToken
from app.auth.repos import AuthRepo
from app.core.constants import PASSWORD_RESET_TOKEN_EXPIRES_IN
from app.core.containers import container
from app.users.models import User

pytestmark = pytest.mark.asyncio


async def test_create_authentication_token(user: User) -> None:
    """Ensure we can create an authentication token."""
    token = await AuthRepo.create_authentication_token(user_id=user.id)

    assert isinstance(token, str)


async def test_get_user_id_from_authentication_token_valid(user: User) -> None:
    """Ensure we can get the user ID from an authentication token."""
    token = await AuthRepo.create_authentication_token(user_id=user.id)

    # Perform token verification
    user_id = await AuthRepo.get_user_id_from_authentication_token(token)

    assert user_id == user.id


async def test_get_user_id_from_authentication_token_invalid() -> None:
    """Ensure we don't get an user ID from an invalid token"""
    user_id = await AuthRepo.get_user_id_from_authentication_token("invalid_token")
    assert user_id is None


async def test_remove_authentication_token(user: User) -> None:
    """Ensure we can remove an authentication token."""
    token = await AuthRepo.create_authentication_token(user_id=user.id)

    # Perform token removal
    await AuthRepo.remove_authentication_token(
        authentication_token=token,
        user_id=user.id,
    )

    # Verify that the token is no longer in Redis
    with container.sync_context() as context:
        redis_client = context.resolve(Redis)
    assert (
        await redis_client.get(
            AuthRepo.generate_authentication_token_key(token),
        )
        is None
    )


# TODO: add tests for remove_all_authentication_tokens

# TODO: add tests for hash_authentication_token

# TODO: add tests for hash_password_reset_token


async def test_create_password_reset_token(user: User) -> None:
    """Ensure a password reset token is created."""

    reset_token = await AuthRepo.create_password_reset_token(
        user_id=user.id,
        last_login_at=user.last_login_at,
    )

    assert isinstance(reset_token, str)


async def test_get_password_reset_token(user: User) -> None:
    """Ensure getting a password reset token works."""
    reset_token = await AuthRepo.create_password_reset_token(
        user_id=user.id,
        last_login_at=user.last_login_at,
    )

    reset_token_hash = sha256(reset_token.encode()).hexdigest()

    retrieved_reset_token = await AuthRepo.get_password_reset_token(
        reset_token_hash=reset_token_hash,
    )

    assert isinstance(retrieved_reset_token, PasswordResetToken)
    assert retrieved_reset_token.token_hash == reset_token_hash
    assert retrieved_reset_token.user_id == user.id
    assert (
        retrieved_reset_token.expires_at - retrieved_reset_token.created_at
        == timedelta(
            seconds=PASSWORD_RESET_TOKEN_EXPIRES_IN,
        )
    )


async def test_get_password_reset_token_not_found() -> None:
    """Ensure getting a non-existent password reset token returns None."""

    reset_token = await AuthRepo.get_password_reset_token(
        reset_token_hash="nonexistent_token",
    )

    assert reset_token is None
