from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.errors import InvalidInputError, ResourceNotFoundError

from .models import User
from .repos import UserRepo


class UserService:
    def __init__(
        self,
        user_repo: UserRepo,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher

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
        current_password: str | None = None,
        new_password: str | None = None,
    ) -> User:
        """Update the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)
        if (
            email
            and await self._user_repo.get_user_by_email(
                email=email,
            )
            is not None
        ):
            raise InvalidInputError(
                message="User with that email already exists.",
            )
        if (
            username
            and await self._user_repo.get_user_by_username(
                username=username,
            )
            is not None
        ):
            raise InvalidInputError(
                message="User with that username already exists.",
            )

        if new_password and current_password:
            try:
                self._password_hasher.verify(
                    hash=user.password_hash,
                    password=current_password,
                )
            except VerifyMismatchError as exception:
                raise InvalidInputError(
                    message="Invalid current password passed.",
                ) from exception
        return await self._user_repo.update_user(
            user=user,
            username=username,
            email=email,
            password=new_password,
        )
