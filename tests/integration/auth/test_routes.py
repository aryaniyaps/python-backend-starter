import pytest
from app.auth.repos import AuthRepo
from app.users.schemas import UserSchema
from fastapi import status
from httpx import AsyncClient

pytestmark = [pytest.mark.anyio]


async def test_register_success(test_client: AsyncClient) -> None:
    """Ensure we can successfully register a new user."""
    response = await test_client.post(
        "/auth/register",
        json={
            "username": "user",
            "email": "user@example.com",
            "password": "password",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


async def test_register_existing_email(
    test_client: AsyncClient,
    user: UserSchema,
) -> None:
    """Ensure we cannot register an user with an existing email."""
    response = await test_client.post(
        "/auth/register",
        json={
            "username": "user",
            "email": user.email,
            "password": "password",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_register_existing_username(
    test_client: AsyncClient,
    user: UserSchema,
) -> None:
    """Ensure we cannot register an user with an existing username."""
    response = await test_client.post(
        "/auth/register",
        json={
            "username": user.username,
            "email": "user@example.com",
            "password": "password",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_login_valid_credentials(
    test_client: AsyncClient,
    user: UserSchema,
) -> None:
    """Ensure we can login a user with valid credentials."""
    response = await test_client.post(
        "/auth/login",
        json={
            "login": user.email,
            "password": "password",
        },
    )

    assert response.status_code == status.HTTP_200_OK


async def test_login_invalid_credentials(
    test_client: AsyncClient,
) -> None:
    """Ensure we cannot login a user with invalid credentials."""
    response = await test_client.post(
        "/auth/login",
        json={
            "login": "invalid_user@example.com",
            "password": "invalid_password",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_login_password_mismatch(
    test_client: AsyncClient,
    user: UserSchema,
) -> None:
    """Ensure we cannot login a user with the wrong password."""
    response = await test_client.post(
        "/auth/login",
        json={
            "login": user.email,
            "password": "wrong_password",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_logout_authenticated_user(
    auth_test_client: AsyncClient,
) -> None:
    """Ensure we can logout an authenticated user."""
    response = await auth_test_client.post("/auth/logout")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_logout_unauthenticated_user(
    test_client: AsyncClient,
) -> None:
    """Ensure we cannot logout an unauthenticated user."""
    logout_response = await test_client.post("/auth/logout")

    assert logout_response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_reset_password_request_success(
    test_client: AsyncClient,
    user: UserSchema,
) -> None:
    """Ensure we can successfully send a password reset request."""
    response = await test_client.post(
        "/auth/reset-password-request",
        json={
            "email": user.email,
        },
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_reset_password_request_nonexistent_user(
    test_client: AsyncClient,
) -> None:
    """Ensure we cannot send a password reset request for a nonexistent user."""
    response = await test_client.post(
        "/auth/reset-password-request",
        json={
            "email": "nonexistent@example.com",
        },
    )

    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    )  # You might want to consider a different status_code code or response behavior


async def test_reset_password_success(
    test_client: AsyncClient,
    user: UserSchema,
    auth_repo: AuthRepo,
) -> None:
    """Ensure we can successfully reset a user's password."""
    reset_token = await auth_repo.create_password_reset_token(
        user_id=user.id,
        last_login_at=user.last_login_at,
    )

    response = await test_client.post(
        "/auth/reset-password",
        json={
            "email": user.email,
            "reset_token": reset_token,
            "new_password": "new_password",
        },
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_reset_password_invalid_token(
    test_client: AsyncClient,
) -> None:
    """Ensure we cannot reset a user's password with an invalid token."""
    response = await test_client.post(
        "/auth/reset-password",
        json={
            "email": "user@example.com",
            "reset_token": "invalid_token",
            "new_password": "new_password",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_reset_password_user_not_found(
    test_client: AsyncClient,
) -> None:
    """Ensure we cannot reset a password for a non-existing user."""
    response = await test_client.post(
        "/auth/reset-password",
        json={
            "email": "nonexistent@example.com",
            "reset_token": "fake_token",
            "new_password": "new_password",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
