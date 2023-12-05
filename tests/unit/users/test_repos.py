import pytest
from sqlalchemy.ext.asyncio import AsyncConnection

from app.users.models import User
from app.users.repos import UserRepo

pytestmark = pytest.mark.asyncio


async def test_create_user(test_connection: AsyncConnection) -> None:
    """Ensure we can create a new user."""
    user = await UserRepo.create_user(
        username="new_user",
        email="new@example.com",
        password_hash="password_hash",
        # TODO: pass connection maker as a parameter here
    )
    assert isinstance(user, User)
    assert user.id is not None
    assert user.username == "new_user"
    assert user.email == "new@example.com"
    # passwords are not hashed in the repository layer
    # the hash must be passed as a value directly
    assert user.password_hash == "password_hash"


async def test_update_user_password(user: User) -> None:
    """Ensure we can update a user's password."""
    updated_user = await UserRepo.update_user_password(
        user_id=user.id,
        password_hash="password_hash",
    )
    assert updated_user
    # passwords are not hashed in the repository layer
    # the hash must be passed as a value directly
    assert updated_user.password_hash == "password_hash"


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
    assert retrieved_user is not None
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


async def test_delete_user(user: User) -> None:
    """Ensure we can delete a user."""
    await UserRepo.delete_user(user_id=user.id)

    retrieved_user = await UserRepo.get_user_by_id(user_id=user.id)
    assert retrieved_user is None


async def test_delete_unknown_user() -> None:
    """Ensure we cannot delete a user by unknown ID."""
    # TODO: check if error is raised here
    await UserRepo.delete_user(user_id=1001)
