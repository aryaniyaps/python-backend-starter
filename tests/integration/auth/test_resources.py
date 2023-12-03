import json

import pytest
from falcon import HTTP_200, HTTP_201, HTTP_204, HTTP_400, HTTP_401
from falcon.testing import ASGIConductor

from app.auth.repos import AuthRepo
from app.auth.services import AuthService
from app.users.models import User

pytestmark = pytest.mark.asyncio


async def test_on_post_register_success(conductor: ASGIConductor) -> None:
    """Ensure we can successfully register a new user."""
    user_data = {
        "username": "user",
        "email": "user@example.com",
        "password": "password",
    }
    response = await conductor.post("/auth/register", body=json.dumps(user_data))

    assert response.status == HTTP_201
    assert "authentication_token" in response.content
    assert "user" in response.content


async def test_on_post_register_existing_email(
    conductor: ASGIConductor, user: User
) -> None:
    """Ensure we cannot register an user with an existing email."""
    user_data = {
        "username": "user",
        "email": user.email,
        "password": "password",
    }
    response = await conductor.post("/auth/register", body=json.dumps(user_data))

    assert response.status == HTTP_400


async def test_on_post_register_existing_username(
    conductor: ASGIConductor, user: User
) -> None:
    """Ensure we cannot register an user with an existing username."""
    user_data = {
        "username": user.username,
        "email": "user@example.com",
        "password": "password",
    }
    response = await conductor.post("/auth/register", body=json.dumps(user_data))

    assert response.status == HTTP_400


async def test_on_post_login_valid_credentials(
    conductor: ASGIConductor, user: User
) -> None:
    """Ensure we can login a user with valid credentials."""
    login_data = {"login": user.email, "password": "password"}
    response = await conductor.post("/auth/login", body=json.dumps(login_data))

    assert response.status == HTTP_200


async def test_on_post_login_invalid_credentials(conductor: ASGIConductor) -> None:
    """Ensure we cannot login a user with invalid credentials."""
    login_data = {"login": "invalid_user@example.com", "password": "invalid_password"}
    response = await conductor.post("/auth/login", body=json.dumps(login_data))

    assert response.status == HTTP_400


async def test_on_post_login_password_mismatch(
    conductor: ASGIConductor, user: User
) -> None:
    """Ensure we cannot login a user with the wrong password."""
    login_data = {"login": user.email, "password": "wrong_password"}
    response = await conductor.post("/auth/login", body=json.dumps(login_data))

    assert response.status == HTTP_400


async def test_on_post_logout_authenticated_user(auth_conductor: ASGIConductor) -> None:
    """Ensure we can logout an authenticated user."""
    response = await auth_conductor.post("/auth/logout")

    assert response.status == HTTP_204


async def test_on_post_logout_unauthenticated_user(conductor: ASGIConductor) -> None:
    """Ensure we cannot logout an unauthenticated user."""
    logout_response = await conductor.post("/auth/logout")

    assert logout_response.status == HTTP_401


async def test_on_post_reset_password_request_success(
    conductor: ASGIConductor, user: User
) -> None:
    """Ensure we can successfully send a password reset request."""
    reset_request_data = {"email": user.email}
    response = await conductor.post(
        "/auth/reset-password-request", body=json.dumps(reset_request_data)
    )

    assert response.status == HTTP_204


async def test_on_post_reset_password_request_nonexistent_user(
    conductor: ASGIConductor,
) -> None:
    """Ensure we cannot send a password reset request for a nonexistent user."""
    reset_request_data = {"email": "nonexistent@example.com"}
    response = await conductor.post(
        "/auth/reset-password-request", body=json.dumps(reset_request_data)
    )

    assert (
        response.status == HTTP_204
    )  # You might want to consider a different status code or response behavior


async def test_on_post_reset_password_success(
    conductor: ASGIConductor, user: User
) -> None:
    """Ensure we can successfully reset a user's password."""
    reset_token = await AuthRepo.create_password_reset_token(
        user_id=user.id,
        user_last_login_at=user.last_login_at,
    )
    reset_data = {
        "email": user.email,
        "reset_token": reset_token,
        "new_password": "new_password",
    }
    # TODO: create a password reset token before testing here
    response = await conductor.post("/auth/reset-password", body=json.dumps(reset_data))

    assert response.status == HTTP_204


async def test_on_post_reset_password_invalid_token(conductor: ASGIConductor) -> None:
    """Ensure we cannot reset a user's password with an invalid token."""
    reset_data = {
        "email": "user@example.com",
        "reset_token": "invalid_token",
        "new_password": "new_password",
    }
    response = await conductor.post("/auth/reset-password", body=json.dumps(reset_data))

    assert response.status == HTTP_400


async def test_on_post_reset_password_user_not_found(conductor: ASGIConductor) -> None:
    """Ensure we cannot reset a password for a non-existing user."""
    reset_data = {
        "email": "nonexistent@example.com",
        "reset_token": "fake_token",
        "new_password": "new_password",
    }
    response = await conductor.post("/auth/reset-password", body=json.dumps(reset_data))

    assert response.status == HTTP_400


async def test_on_post_reset_password_invalid_email(conductor: ASGIConductor) -> None:
    """Ensure we cannot reset a password for an invalid email."""
    reset_data = {
        "email": "invalid_email",
        "reset_token": "fake_token",
        "new_password": "new_password",
    }
    response = await conductor.post("/auth/reset-password", body=json.dumps(reset_data))

    assert response.status == HTTP_400
