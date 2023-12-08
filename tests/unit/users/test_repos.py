from uuid import uuid4

import pytest

from app.core.security import password_hasher
from app.users.models import User
from app.users.repos import UserRepo

pytestmark = pytest.mark.asyncio


async def test_create_user(user_repo: UserRepo) -> None:
    """Ensure we can create a new user."""
    user = await user_repo.create_user(
        username="new_user",
        email="new@example.com",
        password="password",
    )
    assert isinstance(user, User)
    assert user.id is not None
    assert user.username == "new_user"
    assert user.email == "new@example.com"
    assert password_hasher.verify(
        hash=user.password_hash,
        password="password",
    )


async def test_update_user_password(user: User, user_repo: UserRepo) -> None:
    """Ensure we can update a user's password."""
    updated_user = await user_repo.update_user_password(
        user_id=user.id,
        password_hash="password_hash",
    )
    assert updated_user
    # passwords are not hashed in the repository layer
    # the hash must be passed as a value directly
    assert updated_user.password_hash == "password_hash"


async def test_get_user_by_username(user: User, user_repo: UserRepo) -> None:
    """Ensure we can get a user by username."""
    retrieved_user = await user_repo.get_user_by_username(username=user.username)
    assert retrieved_user is not None
    assert retrieved_user == user


async def test_get_user_by_unknown_username(user_repo: UserRepo) -> None:
    """Ensure we cannot get a user by unknown username."""
    retrieved_user = await user_repo.get_user_by_username(username="unknown_username")
    assert retrieved_user is None


async def test_get_user_by_id(user: User, user_repo: UserRepo) -> None:
    """Ensure we can get a user by ID."""
    retrieved_user = await user_repo.get_user_by_id(user_id=user.id)
    assert retrieved_user is not None
    assert retrieved_user == user


async def test_get_user_by_unknown_id(user_repo: UserRepo) -> None:
    """Ensure we cannot get a user by unknown ID."""
    retrieved_user = await user_repo.get_user_by_id(user_id=uuid4())
    assert retrieved_user is None


async def test_get_user_by_email(user: User, user_repo: UserRepo) -> None:
    """Ensure we can get a user by email."""
    retrieved_user = await user_repo.get_user_by_email(email=user.email)
    assert retrieved_user is not None
    assert retrieved_user == user


async def test_get_user_by_unknown_email(user_repo: UserRepo) -> None:
    """Ensure we cannot get a user by unknown email."""
    retrieved_user = await user_repo.get_user_by_email(email="unknown@example.com")
    assert retrieved_user is None


async def test_delete_user(user: User, user_repo: UserRepo) -> None:
    """Ensure we can delete a user."""
    await user_repo.delete_user(user_id=user.id)

    retrieved_user = await user_repo.get_user_by_id(user_id=user.id)
    assert retrieved_user is None


async def test_delete_unknown_user(user_repo: UserRepo) -> None:
    """Ensure we cannot delete a user by unknown ID."""
    # TODO: check if error is raised here
    await user_repo.delete_user(user_id=uuid4())
