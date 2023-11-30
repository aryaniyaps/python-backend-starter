import json
import pytest
from falcon import (
    HTTP_200,
    HTTP_201,
    HTTP_400,
    HTTP_401,
    HTTP_204,
)
from falcon.testing import ASGIConductor

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
