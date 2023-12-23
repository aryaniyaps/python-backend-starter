from uuid import uuid4

import pytest
from sanic_testing.testing import SanicASGITestClient

from app.users.models import User

pytestmark = [pytest.mark.anyio]


async def test_on_get_current_user_authenticated(
    auth_test_client: SanicASGITestClient,
) -> None:
    """Ensure we can successfully get the current user when authenticated."""
    response = await auth_test_client.get("/users/@me")

    assert response.status_code == 200


async def test_on_get_current_user_unauthenticated(
    test_client: SanicASGITestClient,
) -> None:
    """Ensure we cannot get the current user when unauthenticated."""
    response = await test_client.get("/users/@me")

    assert response.status_code == 401


async def test_on_get_user_authenticated(
    auth_test_client: SanicASGITestClient, user: User
) -> None:
    """Ensure we can successfully get a user by ID when authenticated."""
    response = await auth_test_client.get(f"/users/{user.id}")

    assert response.status_code == 200


async def test_on_get_user_unauthenticated(
    test_client: SanicASGITestClient, user: User
) -> None:
    """Ensure we cannot get a user by ID when unauthenticated."""
    response = await test_client.get(f"/users/{user.id}")

    assert response.status_code == 401


async def test_on_get_user_not_found(auth_test_client: SanicASGITestClient) -> None:
    """Ensure getting a non-existent user returns a 404."""
    response = await auth_test_client.get(
        f"/users/{uuid4()}"
    )  # Assuming generated UUID doesn't exist

    assert response.status_code == 404
