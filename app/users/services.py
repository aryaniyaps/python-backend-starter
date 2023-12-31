from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.core.errors import InvalidInputError, ResourceNotFoundError

from .models import User
from .repos import UserRepo


class UserService:
    def __init__(
        self,
        user_repo: Annotated[
            UserRepo,
            Depends(
                dependency=UserRepo,
            ),
        ],
    ) -> None:
        self._user_repo = user_repo

    async def get_user_by_id(self, user_id: UUID) -> User:
        """Get a user by ID."""
        user = await self._user_repo.get_user_by_id(user_id=user_id)
        if user is None:
            raise ResourceNotFoundError(
                message="Couldn't find user with the given ID.",
            )
        return user

    async def update_user(
        self,
        user_id: UUID,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> User:
        """Update the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)
        if (
            email
            and self._user_repo.get_user_by_email(
                email=email,
            )
            is not None
        ):
            raise InvalidInputError(
                message="User with that email already exists.",
            )
        if (
            username
            and self._user_repo.get_user_by_username(
                username=username,
            )
            is not None
        ):
            raise InvalidInputError(
                message="User with that username already exists.",
            )
        return await self._user_repo.update_user(
            user=user,
            username=username,
            email=email,
            password=password,
        )
