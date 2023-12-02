from argon2.exceptions import HashingError, VerifyMismatchError

from app.auth.repos import AuthRepo
from app.core.errors import InvalidInputError, UnauthenticatedError, UnexpectedError
from app.core.security import password_hasher
from app.users.repos import UserRepo

from .models import (
    CreateUserInput,
    CreateUserResult,
    LoginUserInput,
    LoginUserResult,
    PasswordResetInput,
    PasswordResetRequestInput,
)


class AuthService:
    @classmethod
    async def register_user(cls, data: CreateUserInput) -> CreateUserResult:
        """Register a new user."""
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
        except HashingError as exception:
            raise UnexpectedError(
                message="Could not create user. Please try again.",
            ) from exception

        authentication_token = await AuthRepo.create_authentication_token(user=user)
        return CreateUserResult(
            authentication_token=authentication_token,
            user=user,
        )

    @classmethod
    async def login_user(cls, data: LoginUserInput) -> LoginUserResult:
        """
        Check the given credentials and return the
        relevant user if they are valid.
        """
        if "@" in data.login:
            # if "@" is present, assume it's an email
            user = await UserRepo.get_user_by_email(
                email=data.login,
            )
        else:
            # assume it's an username
            user = await UserRepo.get_user_by_username(
                username=data.login,
            )
        if not user:
            raise InvalidInputError(
                message="Invalid credentials provided.",
            )
        try:
            password_hasher.verify(
                hash=user.password,
                password=data.password,
            )
        except VerifyMismatchError as exception:
            raise InvalidInputError(
                message="Invalid credentials provided.",
            ) from exception
        if password_hasher.check_needs_rehash(
            hash=user.password,
        ):
            # update user's password hash
            await UserRepo.update_user_password(
                user_id=user.id,
                password=password_hasher.hash(
                    password=data.password,
                ),
            )
        authentication_token = await AuthRepo.create_authentication_token(user=user)
        return LoginUserResult(
            authentication_token=authentication_token,
            user=user,
        )

    @classmethod
    async def verify_authentication_token(cls, authentication_token: str) -> int:
        """
        Verify the given authentication token and
        return the corresponding user ID.
        """
        user_id = await AuthRepo.verify_authentication_token(
            authentication_token=authentication_token,
        )

        if not user_id:
            raise UnauthenticatedError(
                message="Invalid authentication token provided.",
            )
        return user_id

    @classmethod
    async def remove_authentication_token(cls, authentication_token: str) -> None:
        """Remove the given authentication token."""
        await AuthRepo.remove_authentication_token(
            authentication_token=authentication_token,
        )

    @classmethod
    async def send_password_reset_request(cls, data: PasswordResetRequestInput) -> None:
        """Send a password reset request to the given email."""
        existing_user = await UserRepo.get_user_by_email(email=data.email)
        if existing_user is not None:
            await AuthRepo.create_password_reset_token(
                user_id=existing_user.id,
            )
            # TODO: send password reset email here

    @classmethod
    async def reset_password(cls, data: PasswordResetInput) -> None:
        """Reset the relevant user's password with the given credentials."""
        password_reset_token = await AuthRepo.get_password_reset_token(
            password_reset_token=data.reset_token,
        )

        existing_user = None

        if password_reset_token:
            existing_user = await UserRepo.get_user_by_email(email=data.email)

        if not existing_user or existing_user.email != data.email:
            raise InvalidInputError(
                message="Invalid password reset code or email provided.",
            )

        await UserRepo.update_user_password(
            user_id=existing_user.id,
            password=password_hasher.hash(
                password=data.new_password,
            ),
        )