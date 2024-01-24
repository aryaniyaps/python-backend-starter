import pytest
from app.auth.repos import AuthRepo
from app.auth.services import AuthService
from app.users.repos import UserRepo
from app.users.services import UserService
from argon2 import PasswordHasher
from geoip2.database import Reader


@pytest.fixture
def auth_service(
    auth_repo: AuthRepo,
    user_repo: UserRepo,
    password_hasher: PasswordHasher,
    geoip_reader: Reader,
) -> AuthService:
    """Get the authentication service."""
    return AuthService(
        auth_repo=auth_repo,
        user_repo=user_repo,
        password_hasher=password_hasher,
        geoip_reader=geoip_reader,
    )


@pytest.fixture
def user_service(user_repo: UserRepo) -> UserService:
    """Get the user service."""
    return UserService(user_repo=user_repo)
