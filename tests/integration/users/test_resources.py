import pytest
from falcon import HTTP_200, HTTP_401, HTTP_404
from falcon.testing import ASGIConductor

from app.users.models import User

pytestmark = pytest.mark.asyncio


async def test_on_get_current_user_authenticated(
    auth_conductor: ASGIConductor, user: User
) -> None:
    """Ensure we can successfully get the current user when authenticated."""
    response = await auth_conductor.get("/users/@me")

    assert response.status == HTTP_200
    assert "username" in response.content
    assert response.content == user.model_dump_json()


async def test_on_get_current_user_unauthenticated(conductor: ASGIConductor) -> None:
    """Ensure we cannot get the current user when unauthenticated."""
    response = await conductor.get("/users/@me")

    assert response.status == HTTP_401


async def test_on_get_user_authenticated(
    auth_conductor: ASGIConductor, user: User
) -> None:
    """Ensure we can successfully get a user by ID when authenticated."""
    response = await auth_conductor.get(f"/users/{user.id}")

    assert response.status == HTTP_200
    assert "username" in response.content
    assert response.content == user.model_dump_json()


async def test_on_get_user_unauthenticated(
    conductor: ASGIConductor, user: User
) -> None:
    """Ensure we cannot get a user by ID when unauthenticated."""
    response = await conductor.get(f"/users/{user.id}")

    assert response.status == HTTP_401


async def test_on_get_user_not_found(auth_conductor: ASGIConductor) -> None:
    """Ensure getting a non-existent user returns a 404."""
    response = await auth_conductor.get("/users/101")  # Assuming ID 101 does not exist

    assert response.status == HTTP_404