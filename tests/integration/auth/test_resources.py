import json
import pytest
from falcon import HTTP_200, HTTP_400, HTTP_401, HTTP_204
from falcon.testing import ASGIConductor
from argon2.exceptions import VerifyMismatchError
from unittest.mock import MagicMock, patch
from app.auth.services import AuthService
from app.auth.models import LoginUserResult
from app.core.errors import InvalidInputError, UnauthenticatedError


@pytest.mark.asyncio
async def test_on_post_login_valid_credentials(conductor: ASGIConductor) -> None:
    """Ensure we can login a user with valid credentials."""
    with patch.object(AuthService, "login_user") as mock_login_user:
        mock_result = LoginUserResult(
            authentication_token="fake_token",
            user=MagicMock(),
        )
        mock_login_user.return_value = mock_result

        # Perform the login using the TestClient
        login_data = {
            "login": "user@example.com",
            "password": "password",
        }
        response = await conductor.post(
            "/auth/login",
            body=json.dumps(login_data),
        )

    assert response.status == HTTP_200
    assert json.loads(response.content) == mock_result.model_dump_json()


@pytest.mark.asyncio
async def test_on_post_login_invalid_credentials(conductor: ASGIConductor) -> None:
    """Ensure we cannot login a user with invalid credentials."""
    with patch.object(AuthService, "login_user") as mock_login_user:
        mock_login_user.side_effect = InvalidInputError("Invalid credentials provided.")

        # Perform the login using the TestClient
        login_data = {
            "login": "invalid_user@example.com",
            "password": "invalid_password",
        }
        response = await conductor.post(
            "/auth/login",
            body=json.dumps(login_data),
        )

    assert (
        response.status == HTTP_400
    )  # Adjust the expected status code based on your implementation


@pytest.mark.asyncio
async def test_on_post_login_password_mismatch(conductor: ASGIConductor) -> None:
    """Ensure we cannot login an existing user with the wrong password."""
    with patch.object(AuthService, "login_user") as mock_login_user:
        mock_login_user.side_effect = VerifyMismatchError("Password mismatch")

        # Perform the login using the TestClient
        login_data = {
            "login": "user@example.com",
            "password": "wrong_password",
        }
        response = await conductor.post(
            "/auth/login",
            body=json.dumps(login_data),
        )

    assert (
        response.status == HTTP_400
    )  # Adjust the expected status code based on your implementation


@pytest.mark.asyncio
async def test_on_post_logout_authenticated_user(conductor: ASGIConductor) -> None:
    """Ensure we can logout an authenticated user."""
    with patch.object(AuthService, "remove_authentication_token") as mock_remove_token:
        # Perform the logout using the TestClient
        headers = {
            "X-Authentication-Token": "fake_token",
        }
        response = await conductor.post(
            "/auth/logout",
            headers=headers,
        )

    assert response.status == HTTP_204


@pytest.mark.asyncio
async def test_on_post_logout_unauthenticated_user(conductor: ASGIConductor) -> None:
    """Ensure we cannot logout an unauthenticated user."""
    with patch.object(AuthService, "remove_authentication_token") as mock_remove_token:
        mock_remove_token.side_effect = UnauthenticatedError(
            "Invalid authentication token provided."
        )

        # Perform the logout using the TestClient without providing a token
        response = await conductor.post("/auth/logout")

    assert (
        response.status == HTTP_401
    )  # Adjust the expected status code based on your implementation
