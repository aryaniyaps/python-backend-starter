from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from app.core.errors import ResourceNotFoundError
from app.users.models import User
from app.users.repos import UserRepo
from app.users.services import UserService

pytestmark = pytest.mark.asyncio


async def test_get_user_by_id_success() -> None:
    """Ensure we can retrieve a user by ID."""
    user_id = uuid4()
    expected_user = MagicMock(spec=User, id=user_id)
    with patch.object(UserRepo, "get_user_by_id", return_value=expected_user):
        result = await UserService.get_user_by_id(user_id=user_id)

    assert result == expected_user


async def test_get_user_by_id_not_found() -> None:
    """Ensure ResourceNotFoundError is raised when a user with the given ID is not found."""
    user_id = uuid4()
    with patch.object(UserRepo, "get_user_by_id", return_value=None):
        with pytest.raises(
            ResourceNotFoundError,
            match="Couldn't find user with the given ID.",
        ):
            await UserService.get_user_by_id(user_id=user_id)
