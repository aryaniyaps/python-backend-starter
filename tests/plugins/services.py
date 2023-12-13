import inject
import pytest

from app.auth.services import AuthService
from app.users.services import UserService


@pytest.fixture
def auth_service() -> AuthService:
    """Get the authentication service."""
    return inject.instance(AuthService)


@pytest.fixture
def user_service() -> UserService:
    """Get the user service."""
    return inject.instance(UserService)
