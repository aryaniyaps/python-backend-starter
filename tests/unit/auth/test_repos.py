from datetime import timedelta
from hashlib import sha256

import pytest
from app.auth.models import PasswordResetToken
from app.auth.repos import AuthRepo
from app.core.constants import PASSWORD_RESET_TOKEN_EXPIRES_IN
from app.users.models import User
from redis.asyncio import Redis

pytestmark = [pytest.mark.anyio]


async def test_create_authentication_token(user: User, auth_repo: AuthRepo) -> None:
    """Ensure we can create an authentication token."""
    token = await auth_repo.create_authentication_token(user_id=user.id)

    assert isinstance(token, str)


async def test_get_user_id_from_authentication_token_valid(
    user: User,
    authentication_token: str,
    auth_repo: AuthRepo,
) -> None:
    """Ensure we can get the user ID from an authentication token."""
    # Perform token verification
    user_id = await auth_repo.get_user_id_from_authentication_token(
        authentication_token=authentication_token,
    )

    assert user_id == user.id


async def test_get_user_id_from_authentication_token_invalid(
    auth_repo: AuthRepo,
) -> None:
    """Ensure we don't get an user ID from an invalid token"""
    user_id = await auth_repo.get_user_id_from_authentication_token("invalid_token")
    assert user_id is None


async def test_remove_authentication_token(
    user: User,
    auth_repo: AuthRepo,
    redis_client: Redis,
) -> None:
    """Ensure we can remove an authentication token."""
    token = await auth_repo.create_authentication_token(user_id=user.id)

    # Perform token removal
    await auth_repo.remove_authentication_token(
        authentication_token=token,
        user_id=user.id,
    )

    # Verify that the token is no longer in Redis
    assert (
        await redis_client.get(
            auth_repo.generate_authentication_token_key(token),
        )
        is None
    )


async def test_remove_all_authentication_tokens(
    user: User,
    auth_repo: AuthRepo,
    redis_client: Redis,
) -> None:
    """Ensure all authentication tokens for a user are removed."""
    first_token = await auth_repo.create_authentication_token(user_id=user.id)

    second_token = await auth_repo.create_authentication_token(user_id=user.id)

    # Perform removal of all authentication tokens
    await auth_repo.remove_all_authentication_tokens(user_id=user.id)

    # Verify that both tokens are no longer in Redis
    assert (
        await redis_client.get(
            auth_repo.generate_authentication_token_key(first_token),
        )
        is None
    )
    assert (
        await redis_client.get(
            auth_repo.generate_authentication_token_key(second_token),
        )
        is None
    )
    assert not (
        await redis_client.smembers(
            auth_repo.generate_token_owner_key(user_id=user.id),
        )  # type: ignore
    )


def test_hash_authentication_token() -> None:
    """Ensure hashing authentication token produces the expected result."""
    token = "test_token"
    expected_hash = sha256(token.encode()).hexdigest()

    hashed_token = AuthRepo.hash_authentication_token(token)

    assert hashed_token == expected_hash


def test_hash_password_reset_token() -> None:
    """Ensure hashing password reset token produces the expected result."""
    reset_token = "test_reset_token"
    expected_hash = sha256(reset_token.encode()).hexdigest()

    hashed_reset_token = AuthRepo.hash_password_reset_token(reset_token)

    assert hashed_reset_token == expected_hash


async def test_create_password_reset_token(user: User, auth_repo: AuthRepo) -> None:
    """Ensure a password reset token is created."""

    reset_token = await auth_repo.create_password_reset_token(
        user_id=user.id,
        last_login_at=user.last_login_at,
    )

    assert isinstance(reset_token, str)


async def test_get_password_reset_token(user: User, auth_repo: AuthRepo) -> None:
    """Ensure getting a password reset token works."""
    reset_token = await auth_repo.create_password_reset_token(
        user_id=user.id,
        last_login_at=user.last_login_at,
    )

    reset_token_hash = sha256(reset_token.encode()).hexdigest()

    retrieved_reset_token = await auth_repo.get_password_reset_token(
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


async def test_get_password_reset_token_not_found(auth_repo: AuthRepo) -> None:
    """Ensure getting a non-existent password reset token returns None."""

    reset_token = await auth_repo.get_password_reset_token(
        reset_token_hash="nonexistent_token",
    )

    assert reset_token is None
