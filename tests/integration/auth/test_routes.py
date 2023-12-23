import pytest
from sanic_testing.testing import SanicASGITestClient

from app.auth.repos import AuthRepo
from app.users.models import User

pytestmark = [pytest.mark.anyio]


async def test_on_post_register_success(test_client: SanicASGITestClient) -> None:
    """Ensure we can successfully register a new user."""
    user_data = {
        "username": "user",
        "email": "user@example.com",
        "password": "password",
    }
    response = await test_client.post(
        "/auth/register",
        data=user_data,
    )

    assert response.status_code == 201


async def test_on_post_register_existing_email(
    test_client: SanicASGITestClient, user: User
) -> None:
    """Ensure we cannot register an user with an existing email."""
    user_data = {
        "username": "user",
        "email": user.email,
        "password": "password",
    }
    response = await test_client.post(
        "/auth/register",
        data=user_data,
    )

    assert response.status_code == 400


async def test_on_post_register_existing_username(
    test_client: SanicASGITestClient, user: User
) -> None:
    """Ensure we cannot register an user with an existing username."""
    user_data = {
        "username": user.username,
        "email": "user@example.com",
        "password": "password",
    }
    response = await test_client.post(
        "/auth/register",
        data=user_data,
    )

    assert response.status_code == 400


async def test_on_post_login_valid_credentials(
    test_client: SanicASGITestClient, user: User
) -> None:
    """Ensure we can login a user with valid credentials."""
    login_data = {"login": user.email, "password": "password"}
    response = await test_client.post(
        "/auth/login",
        data=login_data,
    )

    assert response.status_code == 200


async def test_on_post_login_invalid_credentials(
    test_client: SanicASGITestClient,
) -> None:
    """Ensure we cannot login a user with invalid credentials."""
    login_data = {"login": "invalid_user@example.com", "password": "invalid_password"}
    response = await test_client.post(
        "/auth/login",
        data=login_data,
    )

    assert response.status_code == 400


async def test_on_post_login_password_mismatch(
    test_client: SanicASGITestClient, user: User
) -> None:
    """Ensure we cannot login a user with the wrong password."""
    login_data = {"login": user.email, "password": "wrong_password"}
    response = await test_client.post(
        "/auth/login",
        data=login_data,
    )

    assert response.status_code == 400


async def test_on_post_logout_authenticated_user(
    auth_test_client: SanicASGITestClient,
) -> None:
    """Ensure we can logout an authenticated user."""
    response = await auth_test_client.post("/auth/logout")

    assert response.status_code == 204


async def test_on_post_logout_unauthenticated_user(
    test_client: SanicASGITestClient,
) -> None:
    """Ensure we cannot logout an unauthenticated user."""
    logout_response = await test_client.post("/auth/logout")

    assert logout_response.status_code == 401


async def test_on_post_reset_password_request_success(
    test_client: SanicASGITestClient, user: User
) -> None:
    """Ensure we can successfully send a password reset request."""
    reset_request_data = {"email": user.email}
    response = await test_client.post(
        "/auth/reset-password-request",
        data=reset_request_data,
    )

    assert response.status_code == 204


async def test_on_post_reset_password_request_nonexistent_user(
    test_client: SanicASGITestClient,
) -> None:
    """Ensure we cannot send a password reset request for a nonexistent user."""
    reset_request_data = {"email": "nonexistent@example.com"}
    response = await test_client.post(
        "/auth/reset-password-request",
        data=reset_request_data,
    )

    assert (
        response.status_code == 204
    )  # You might want to consider a different status_code code or response behavior


async def test_on_post_reset_password_success(
    test_client: SanicASGITestClient, user: User, auth_repo: AuthRepo
) -> None:
    """Ensure we can successfully reset a user's password."""
    reset_token = await auth_repo.create_password_reset_token(
        user_id=user.id,
        last_login_at=user.last_login_at,
    )
    reset_data = {
        "email": user.email,
        "reset_token": reset_token,
        "new_password": "new_password",
    }

    response = await test_client.post(
        "/auth/reset-password",
        data=reset_data,
    )

    assert response.status_code == 204


async def test_on_post_reset_password_invalid_token(
    test_client: SanicASGITestClient,
) -> None:
    """Ensure we cannot reset a user's password with an invalid token."""
    reset_data = {
        "email": "user@example.com",
        "reset_token": "invalid_token",
        "new_password": "new_password",
    }
    response = await test_client.post(
        "/auth/reset-password",
        data=reset_data,
    )

    assert response.status_code == 400


async def test_on_post_reset_password_user_not_found(
    test_client: SanicASGITestClient,
) -> None:
    """Ensure we cannot reset a password for a non-existing user."""
    reset_data = {
        "email": "nonexistent@example.com",
        "reset_token": "fake_token",
        "new_password": "new_password",
    }
    response = await test_client.post(
        "/auth/reset-password",
        data=reset_data,
    )

    assert response.status_code == 400


async def test_on_post_reset_password_invalid_email(
    test_client: SanicASGITestClient,
) -> None:
    """Ensure we cannot reset a password for an invalid email."""
    reset_data = {
        "email": "invalid_email",
        "reset_token": "fake_token",
        "new_password": "new_password",
    }
    response = await test_client.post(
        "/auth/reset-password",
        data=reset_data,
    )

    assert response.status_code == 400
