import pytest
from falcon.asgi import App

from app import create_app
from app.core.security import password_hasher
from app.users.models import User
from app.users.repos import UserRepo


@pytest.fixture(scope="session")
def app() -> App:
    """Initialize the app for testing."""
    return create_app()


@pytest.fixture(scope="session")
async def user() -> User:
    """Create an user for testing."""
    # TODO: cleanup user after testing
    return await UserRepo.create_user(
        username="tester",
        email="tester@example.org",
        password=password_hasher.hash(
            password="password",
        ),
    )
