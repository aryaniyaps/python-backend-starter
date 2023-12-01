import pytest
from app.users.repos import UserRepo
from app.users.models import User

pytestmark = pytest.mark.asyncio


async def test_create_user() -> None:
    """Ensure we can create a new user."""
    user = await UserRepo.create_user(
        username="new_user",
        email="new@example.com",
        password="new_password",
    )
    assert isinstance(user, User)
    assert user.id is not None
    assert user.username == "new_user"
    assert user.email == "new@example.com"
    # passwords are not hashed in the repository layer
    # the hash must be passed as a value directly
    assert user.password == "new_password"


async def test_update_user_password(user: User) -> None:
    """Ensure we can update a user's password."""
    updated_user = await UserRepo.update_user_password(
        user_id=user.id,
        password="new_password",
    )
    assert updated_user
    # passwords are not hashed in the repository layer
    # the hash must be passed as a value directly
    assert updated_user.password == "new_password"


async def test_get_user_by_username(user: User) -> None:
    """Ensure we can get a user by username."""
    retrieved_user = await UserRepo.get_user_by_username(username=user.username)
    assert retrieved_user
    assert retrieved_user == user


async def test_get_user_by_unknown_username() -> None:
    """Ensure we cannot get a user by unknown username."""
    retrieved_user = await UserRepo.get_user_by_username(username="unknown_username")
    assert retrieved_user is None


async def test_get_user_by_id(user: User) -> None:
    """Ensure we can get a user by ID."""
    retrieved_user = await UserRepo.get_user_by_id(user_id=user.id)
    assert retrieved_user
    assert retrieved_user == user


async def test_get_user_by_unknown_id() -> None:
    """Ensure we cannot get a user by unknown ID."""
    retrieved_user = await UserRepo.get_user_by_id(user_id=1001)
    assert retrieved_user is None


async def test_get_user_by_email(user: User) -> None:
    """Ensure we can get a user by email."""
    retrieved_user = await UserRepo.get_user_by_email(email=user.email)
    assert retrieved_user
    assert retrieved_user == user


async def test_get_user_by_unknown_email() -> None:
    """Ensure we cannot get a user by unknown email."""
    retrieved_user = await UserRepo.get_user_by_email(email="unknown@example.com")
    assert retrieved_user is None
