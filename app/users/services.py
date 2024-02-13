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
    ) -> User:
        """Update the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)
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
        return await self._user_repo.update_user(
            user=user,
            username=username,
        )

    async def update_user_password(
        self,
        user_id: UUID,
        new_password: str,
        current_password: str,
    ) -> User:
        """Update the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)

        try:
            self._password_hasher.verify(
                hash=user.password_hash,
                password=current_password,
            )
        except VerifyMismatchError as exception:
            raise InvalidInputError(
                message="Invalid current password provided.",
            ) from exception

        return await self._user_repo.update_user(
            user=user,
            password=new_password,
        )

    async def update_user_email(
        self,
        user_id: UUID,
        email: str,
    ) -> None:
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

        # TODO: send email change verification code
        # return await self._user_repo.update_user(
        #     user=user,
        #     email=email,
        # )
