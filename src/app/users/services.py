from app.core.errors import ResourceNotFoundError

from .models import User
from .repos import UserRepo

from app.core.security import password_hasher


class UserService:
    @classmethod
    async def get_user_by_id(cls, user_id: int) -> User:
        """Get a user by ID."""
        user = await UserRepo.get_user_by_id(user_id=user_id)
        if not user:
            raise ResourceNotFoundError(
                message="Couldn't find user with the given ID.",
            )
        return user
