from typing import Annotated
from uuid import UUID
from xml.dom import InvalidAccessErr

from fastapi import Depends

from app.core.errors import InvalidInputError, ResourceNotFoundError

from .models import UpdateUserInput, User
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

    async def update_user(self, user_id: UUID, data: UpdateUserInput) -> User:
        """Update the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)
        if data.email and self._user_repo.get_user_by_email(email=data.email):
            raise InvalidInputError(
                message="User with that email already exists.",
            )
        if data.username and self._user_repo.get_user_by_username(
            username=data.username
        ):
            raise InvalidInputError(
                message="User with that username already exists.",
            )
        return await self._user_repo.update_user(
            user_id=user.id,
            username=data.username,
            email=data.email,
            password=data.password,
        )
