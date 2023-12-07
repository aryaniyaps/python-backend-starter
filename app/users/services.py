from uuid import UUID

from app.core.errors import ResourceNotFoundError

from .models import User
from .repos import UserRepo


class UserService:
    @classmethod
    async def get_user_by_id(cls, user_id: UUID) -> User:
        """Get a user by ID."""
        user = await UserRepo.get_user_by_id(user_id=user_id)
        if user is None:
            raise ResourceNotFoundError(
                message="Couldn't find user with the given ID.",
            )
        return user
