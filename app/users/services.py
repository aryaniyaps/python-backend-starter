from uuid import UUID

import inject

from app.core.errors import ResourceNotFoundError

from .models import User
from .repos import UserRepo


class UserService:
    _user_repo = inject.attr(UserRepo)

    async def get_user_by_id(self, user_id: UUID) -> User:
        """Get a user by ID."""
        user = await self._user_repo.get_user_by_id(user_id=user_id)
        if user is None:
            raise ResourceNotFoundError(
                message="Couldn't find user with the given ID.",
            )
        return user
