from uuid import uuid4

import pytest
from app.users.models import User
from app.users.repos import UserRepo
from argon2 import PasswordHasher

pytestmark = [pytest.mark.anyio]


async def test_create_user(
    user_repo: UserRepo,
    password_hasher: PasswordHasher,
) -> None:
    """Ensure we can create a new user."""
    user = await user_repo.create(
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


async def test_update_user_password(
    user: User,
    user_repo: UserRepo,
    password_hasher: PasswordHasher,
) -> None:
    """Ensure we can update a user's password."""
    updated_user = await user_repo.update(
        user=user,
        password="password",
    )
    assert password_hasher.verify(
        hash=updated_user.password_hash,
        password="password",
    )
    assert updated_user.updated_at is not None


async def test_update_user_username(
    user: User,
    user_repo: UserRepo,
) -> None:
    """Ensure we can update a user's username."""
    updated_user = await user_repo.update(
        user=user,
        username="new_username",
    )
    assert updated_user.username == "new_username"
    assert updated_user.updated_at is not None


async def test_update_user_email(
    user: User,
    user_repo: UserRepo,
) -> None:
    """Ensure we can update a user's email."""
    updated_user = await user_repo.update(
        user=user,
        email="new_email@example.com",
    )
    assert updated_user.email == "new_email@example.com"
    assert updated_user.updated_at is not None


async def test_get_user_by_username(user: User, user_repo: UserRepo) -> None:
    """Ensure we can get a user by username."""
    retrieved_user = await user_repo.get_by_username(username=user.username)
    assert retrieved_user is not None
    assert retrieved_user == user


async def test_get_user_by_username_case_insensitive(
    user: User, user_repo: UserRepo
) -> None:
    """Ensure retrieving a user by username is case-insensitive."""
    retrieved_user_lower = await user_repo.get_by_username(
        username=user.username.lower()
    )
    retrieved_user_upper = await user_repo.get_by_username(
        username=user.username.upper()
    )

    assert retrieved_user_lower == retrieved_user_upper == user


async def test_get_user_by_unknown_username(user_repo: UserRepo) -> None:
    """Ensure we cannot get a user by unknown username."""
    retrieved_user = await user_repo.get_by_username(username="unknown_username")
    assert retrieved_user is None


async def test_get_user_by_id(user: User, user_repo: UserRepo) -> None:
    """Ensure we can get a user by ID."""
    retrieved_user = await user_repo.get(user_id=user.id)
    assert retrieved_user is not None
    assert retrieved_user == user


async def test_get_user_by_unknown_id(user_repo: UserRepo) -> None:
    """Ensure we cannot get a user by unknown ID."""
    retrieved_user = await user_repo.get(user_id=uuid4())
    assert retrieved_user is None


async def test_get_user_by_email(user: User, user_repo: UserRepo) -> None:
    """Ensure we can get a user by email."""
    retrieved_user = await user_repo.get_by_email(email=user.email)
    assert retrieved_user is not None
    assert retrieved_user == user


async def test_get_user_by_email_case_insensitive(
    user: User, user_repo: UserRepo
) -> None:
    """Ensure retrieving a user by email is case-insensitive."""
    retrieved_user_lower = await user_repo.get_by_email(email=user.email.lower())
    retrieved_user_upper = await user_repo.get_by_email(email=user.email.upper())

    assert retrieved_user_lower == retrieved_user_upper == user


async def test_get_user_by_unknown_email(user_repo: UserRepo) -> None:
    """Ensure we cannot get a user by unknown email."""
    retrieved_user = await user_repo.get_by_email(email="unknown@example.com")
    assert retrieved_user is None
