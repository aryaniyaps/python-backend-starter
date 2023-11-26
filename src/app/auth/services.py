from argon2.exceptions import VerifyMismatchError
from app.auth.repos import AuthRepo

from app.core.errors import InvalidInputError, UnauthenticatedError

from .models import LoginUserInput, LoginUserResult

from app.users.repos import UserRepo

from app.core.security import password_hasher


class AuthService:
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
        except VerifyMismatchError:
            raise InvalidInputError(
                message="Invalid credentials provided.",
            )
        else:
            if password_hasher.check_needs_rehash(
                hash=user.password,
            ):
                # update user's password hash
                await UserRepo.update_user(
                    user_id=user.id,
                    password=password_hasher.hash(
                        password=data.password,
                    ),
                )
            token = await AuthRepo.create_authentication_token(user=user)
            return LoginUserResult(
                token=token,
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
                message="Invalid or expired token",
            )
        return user_id

    @classmethod
    async def remove_authentication_token(cls, authentication_token: str) -> None:
        """Remove the given authentication token."""
        await AuthRepo.remove_authentication_token(
            authentication_token=authentication_token,
        )
