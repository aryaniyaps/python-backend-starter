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
    user = await user_repo.create_user(
        username="new_user",
        email="new@example.com",
        password="password",
        login_ip="127.0.0.1",
    )
    assert isinstance(user, User)
    assert user.id is not None
    assert user.username == "new_user"
    assert user.email == "new@example.com"
    assert user.last_login_ip == "127.0.0.1"
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
    updated_user = await user_repo.update_user(
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
    updated_user = await user_repo.update_user(
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
    updated_user = await user_repo.update_user(
        user=user,
        email="new_email@example.com",
    )
    assert updated_user.email == "new_email@example.com"
    assert updated_user.updated_at is not None


async def test_update_user_last_login_ip(
    user: User,
    user_repo: UserRepo,
) -> None:
    """Ensure we can update a user's last login IP."""
    updated_user = await user_repo.update_user(
        user=user,
        last_login_ip="208.80.154.224",
    )
    assert updated_user.last_login_ip == "208.80.154.224"
    assert updated_user.updated_at is not None


async def test_update_user_last_login_at(
    user: User,
    user_repo: UserRepo,
) -> None:
    """Ensure we can update a user's last login timestamp."""
    initial_last_login_at = user.last_login_at
    updated_user = await user_repo.update_user(
        user=user,
        update_last_login=True,
    )

    # THIS TEST CASE IS FAILING BECAUSE THE USER FIXTURE CREATE STATEMENT AND
    # THE UPDATE STATEMENT ARE EXECUTED WITHIN THE SAME TRANSACTION. THEREFORE
    # NOW() RETURNS THE SAME TIMESTAMP
    # FOR A DIFFERENT TIMESTAMP WE MUST USE `clock_timestamp()` OR `statement_timestamp()`
    # GIVEN BY POSTGRESQL

    # ALTERNATIVELY, WE CAN CREATE THE USER IN A DIFFERENT TRANSACTION ITSELF
    # THIS MIMICKS THE REAL LIFE SCENARIO MORE CORRECTLY
    assert updated_user.last_login_at > initial_last_login_at
    assert updated_user.updated_at is not None


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
