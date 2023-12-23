import pytest
from argon2 import PasswordHasher

from app.auth.repos import AuthRepo
from app.auth.services import AuthService
from app.users.repos import UserRepo
from app.users.services import UserService


@pytest.fixture
def auth_service(
    auth_repo: AuthRepo,
    user_repo: UserRepo,
    password_hasher: PasswordHasher,
) -> AuthService:
    """Get the authentication service."""
    return AuthService(
        auth_repo=auth_repo,
        user_repo=user_repo,
        password_hasher=password_hasher,
    )


@pytest.fixture
def user_service(user_repo: UserRepo) -> UserService:
    """Get the user service."""
    return UserService(user_repo=user_repo)
