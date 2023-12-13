import inject
import pytest

from app.auth.repos import AuthRepo
from app.users.repos import UserRepo


@pytest.fixture
def auth_repo() -> AuthRepo:
    """Get the authentication repository."""
    return inject.instance(AuthRepo)


@pytest.fixture
def user_repo() -> UserRepo:
    """Get the user repository."""
    return inject.instance(UserRepo)
