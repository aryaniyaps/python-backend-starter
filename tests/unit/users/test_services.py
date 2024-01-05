from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from app.core.errors import InvalidInputError, ResourceNotFoundError
from app.users.models import User
from app.users.repos import UserRepo
from app.users.services import UserService

pytestmark = [pytest.mark.anyio]


async def test_get_user_by_id_success(user_service: UserService) -> None:
    """Ensure we can retrieve a user by ID."""
    user_id = uuid4()
    expected_user = MagicMock(spec=User, id=user_id)
    with patch.object(UserRepo, "get_user_by_id", return_value=expected_user):
        result = await user_service.get_user_by_id(user_id=user_id)

    assert result == expected_user


async def test_get_user_by_id_not_found(user_service: UserService) -> None:
    """Ensure ResourceNotFoundError is raised when a user with the given ID is not found."""
    user_id = uuid4()
    with patch.object(
        UserRepo,
        "get_user_by_id",
        return_value=None,
    ):
        with pytest.raises(
            ResourceNotFoundError,
            match="Couldn't find user with the given ID.",
        ):
            await user_service.get_user_by_id(user_id=user_id)


async def test_update_user_success(user_service: UserService) -> None:
    """Ensure we can update a user successfully."""
    user_id = uuid4()

    existing_user = MagicMock(spec=User, id=user_id)
    with patch.object(
        UserService,
        "get_user_by_id",
        return_value=existing_user,
    ), patch.object(
        UserRepo,
        "get_user_by_email",
        return_value=None,
    ), patch.object(
        UserRepo,
        "get_user_by_username",
        return_value=None,
    ), patch.object(
        UserRepo,
        "update_user",
        return_value=existing_user,
    ):
        result = await user_service.update_user(
            user_id=user_id,
            username="new_username",
            email="new_email@example.com",
            password="new_password",
        )

    assert result == existing_user


async def test_update_user_email_exists(user_service: UserService) -> None:
    """Ensure InvalidInputError is raised when trying to update user with an existing email."""
    user_id = uuid4()

    existing_user = MagicMock(spec=User, id=user_id)
    with patch.object(
        UserService,
        "get_user_by_id",
        return_value=existing_user,
    ), patch.object(
        UserRepo,
        "get_user_by_email",
        return_value=MagicMock(
            spec=User,
            email="existing_email@example.com",
        ),
    ):
        with pytest.raises(
            InvalidInputError, match="User with that email already exists."
        ):
            await user_service.update_user(
                user_id=user_id,
                email="existing_email@example.com",
            )


async def test_update_user_username_exists(user_service: UserService) -> None:
    """Ensure InvalidInputError is raised when trying to update user with an existing username."""
    user_id = uuid4()

    existing_user = MagicMock(spec=User, id=user_id)
    with patch.object(UserService, "get_user_by_id", return_value=existing_user):
        with patch.object(
            UserRepo, "get_user_by_username", return_value=MagicMock()
        ), pytest.raises(
            InvalidInputError, match="User with that username already exists."
        ):
            await user_service.update_user(
                user_id=user_id,
                username="existing_username",
            )


async def test_update_user_not_found(user_service: UserService) -> None:
    """Ensure ResourceNotFoundError is raised when trying to update a non-existing user."""
    user_id = uuid4()

    with patch.object(
        UserRepo,
        "get_user_by_id",
        return_value=None,
    ):
        with pytest.raises(
            ResourceNotFoundError,
            match="Couldn't find user with the given ID.",
        ):
            await user_service.update_user(
                user_id=user_id,
                username="new_username",
                email="new_email@example.com",
                password="new_password",
            )
