from argon2.exceptions import HashingError
from app.auth.repos import AuthRepo

from app.core.errors import InvalidInputError, ResourceNotFoundError, UnexpectedError

from .models import CreateUserResult, CreateUserInput, User
from .repos import UserRepo

from app.core.security import password_hasher


class UserService:
    @classmethod
    async def create_user(cls, data: CreateUserInput) -> CreateUserResult:
        """Create a new user."""
        try:
            if (
                await UserRepo.get_user_by_email(
                    email=data.email,
                )
                is not None
            ):
                raise InvalidInputError(
                    message="User with that email already exists.",
                )
            if (
                await UserRepo.get_user_by_username(
                    username=data.username,
                )
                is not None
            ):
                raise InvalidInputError(
                    message="User with that username already exists.",
                )
            user = await UserRepo.create_user(
                username=data.username,
                email=data.email,
                # hash password before storing
                password=password_hasher.hash(
                    password=data.password,
                ),
            )
        except HashingError:
            raise UnexpectedError(
                message="Could not create user. Please try again.",
            )
        else:
            authentication_token = await AuthRepo.create_authentication_token(user=user)
            return CreateUserResult(
                authentication_token=authentication_token,
                user=user,
            )

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> User:
        """Get a user by ID."""
        user = await UserRepo.get_user_by_id(user_id=user_id)
        if not user:
            raise ResourceNotFoundError(
                message="Couldn't find user with the given ID.",
            )
        return user
