from http import HTTPStatus
from uuid import uuid4

import pytest
from app.users.schemas import UserSchema
from httpx import AsyncClient

pytestmark = [pytest.mark.anyio]


async def test_get_current_user_authenticated(
    auth_test_client: AsyncClient,
) -> None:
    """Ensure we can successfully get the current user when authenticated."""
    response = await auth_test_client.get("/users/@me")

    assert response.status_code == HTTPStatus.OK


async def test_get_current_user_unauthenticated(
    test_client: AsyncClient,
) -> None:
    """Ensure we cannot get the current user when unauthenticated."""
    response = await test_client.get("/users/@me")

    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_get_user_authenticated(
    auth_test_client: AsyncClient,
    user: UserSchema,
) -> None:
    """Ensure we can successfully get a user by ID when authenticated."""
    response = await auth_test_client.get(f"/users/{user.id}")

    assert response.status_code == HTTPStatus.OK


async def test_get_user_not_found(auth_test_client: AsyncClient) -> None:
    """Ensure getting a non-existent user returns a 404."""
    response = await auth_test_client.get(
        f"/users/{uuid4()}",
    )  # Assuming generated UUID doesn't exist

    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_update_current_user_authenticated(auth_test_client: AsyncClient) -> None:
    """Ensure we can successfully update the current user when authenticated."""
    response = await auth_test_client.patch(
        "/users/@me",
        json={
            "username": "new_username",
            "email": "new_email@example.com",
            "password": "newPassword12!",
        },
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data["username"] == "new_username"
    assert data["email"] == "new_email@example.com"


async def test_update_current_user_unauthenticated(
    test_client: AsyncClient,
) -> None:
    """Ensure we cannot update the current user when unauthenticated."""
    new_data = {
        "username": "new_username",
        "email": "new_email@example.com",
        "password": "newPassword12!",
    }
    response = await test_client.patch("/users/@me", json=new_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_update_current_user_invalid_input(auth_test_client: AsyncClient) -> None:
    """Ensure updating the current user with invalid input returns a 422 Unprocessable Entity."""
    response = await auth_test_client.patch(
        "/users/@me",
        json={
            "email": "invalid_email",
        },  # Assuming this is an invalid email
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_update_current_user_existing_email(
    auth_test_client: AsyncClient,
    user: UserSchema,
) -> None:
    """Ensure we cannot update the current user with an existing email."""
    response = await auth_test_client.patch(
        "/users/@me",
        json={
            "email": user.email,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


async def test_update_current_user_existing_username(
    auth_test_client: AsyncClient,
    user: UserSchema,
) -> None:
    """Ensure we cannot update the current user with an existing username."""
    response = await auth_test_client.patch(
        "/users/@me",
        json={
            "username": user.username,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
