from typing import AsyncIterator
from falcon.asgi import App
from falcon.testing import TestClient, ASGIConductor
import pytest

from app import create_app
from app.auth.repos import AuthRepo
from app.users.models import User
from app.users.repos import UserRepo


@pytest.fixture(scope="session")
def app() -> App:
    """Initialize the app for testing."""
    return create_app()


@pytest.fixture(scope="session")
def test_client(app: App) -> TestClient:
    """Initialize the test client."""
    return TestClient(app)


@pytest.fixture(scope="function")
async def conductor(test_client: TestClient) -> AsyncIterator[ASGIConductor]:
    """Initialize the test conductor for the ASGI app."""
    async with test_client as conductor:
        yield conductor


@pytest.fixture(scope="session")
async def auth_test_client(app: App, user: User) -> TestClient:
    """Initialize an authenticated test client for testing."""
    authentication_token = await AuthRepo.create_authentication_token(user=user)
    return TestClient(
        app,
        headers={
            "X-Authentication-Token": authentication_token,
        },
    )


@pytest.fixture(scope="session")
async def user() -> User:
    """Create an user for testing."""
    return await UserRepo.create_user(
        username="tester",
        email="tester@example.org",
        password="password",
    )
