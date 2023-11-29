import json
import pytest
from falcon import (
    HTTP_200,
    HTTP_400,
    HTTP_401,
    HTTP_204,
)
from falcon.testing import ASGIConductor


@pytest.mark.asyncio
async def test_on_post_login_valid_credentials(conductor: ASGIConductor, user) -> None:
    """Ensure we can login a user with valid credentials."""
    login_data = {"login": user.email, "password": "password"}
    response = await conductor.post("/auth/login", body=json.dumps(login_data))

    assert response.status == HTTP_200


@pytest.mark.asyncio
async def test_on_post_login_invalid_credentials(conductor: ASGIConductor) -> None:
    """Ensure we cannot login a user with invalid credentials."""
    login_data = {"login": "invalid_user@example.com", "password": "invalid_password"}
    response = await conductor.post("/auth/login", body=json.dumps(login_data))

    assert response.status == HTTP_400


@pytest.mark.asyncio
async def test_on_post_login_password_mismatch(conductor: ASGIConductor, user) -> None:
    """Ensure we cannot login a user with the wrong password."""
    login_data = {"login": user.email, "password": "wrong_password"}
    response = await conductor.post("/auth/login", body=json.dumps(login_data))

    assert response.status == HTTP_400


@pytest.mark.asyncio
async def test_on_post_logout_authenticated_user(auth_conductor: ASGIConductor) -> None:
    """Ensure we can logout an authenticated user."""
    response = await auth_conductor.post("/auth/logout")

    assert response.status == HTTP_204


@pytest.mark.asyncio
async def test_on_post_logout_unauthenticated_user(conductor: ASGIConductor) -> None:
    """Ensure we cannot logout an unauthenticated user."""
    logout_response = await conductor.post("/auth/logout")

    assert logout_response.status == HTTP_401
