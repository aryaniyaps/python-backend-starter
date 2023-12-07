from hashlib import sha256
from uuid import UUID

from argon2.exceptions import HashingError, VerifyMismatchError
from user_agents.parsers import UserAgent

from app.auth.repos import AuthRepo
from app.auth.tasks import send_password_reset_request_email
from app.core.errors import InvalidInputError, UnauthenticatedError, UnexpectedError
from app.core.security import password_hasher
from app.users.repos import UserRepo

from .models import (
    CreateUserResult,
    LoginUserInput,
    LoginUserResult,
    PasswordResetInput,
    PasswordResetRequestInput,
    RegisterUserInput,
)


class AuthService:
    def __init__(
        self,
        auth_repo: AuthRepo,
        user_repo: UserRepo,
    ) -> None:
        self._auth_repo = auth_repo
        self._user_repo = user_repo

    async def register_user(self, data: RegisterUserInput) -> CreateUserResult:
        """Register a new user."""
        try:
            if (
                await self._user_repo.get_user_by_email(
                    email=data.email,
                )
                is not None
            ):
                raise InvalidInputError(
                    message="User with that email already exists.",
                )
            if (
                await self._user_repo.get_user_by_username(
                    username=data.username,
                )
                is not None
            ):
                raise InvalidInputError(
                    message="User with that username already exists.",
                )
            user = await self._user_repo.create_user(
                username=data.username,
                email=data.email,
                password=data.password,
            )
        except HashingError as exception:
            raise UnexpectedError(
                message="Could not create user. Please try again.",
            ) from exception

        authentication_token = await self._auth_repo.create_authentication_token(
            user_id=user.id
        )
        return CreateUserResult(
            authentication_token=authentication_token,
            user=user,
        )

    async def login_user(self, data: LoginUserInput) -> LoginUserResult:
        """
        Check the given credentials and return the
        relevant user if they are valid.
        """
        if "@" in data.login:
            # if "@" is present, assume it's an email
            user = await self._user_repo.get_user_by_email(
                email=data.login,
            )
        else:
            # assume it's an username
            user = await self._user_repo.get_user_by_username(
                username=data.login,
            )
        if not user:
            raise InvalidInputError(
                message="Invalid credentials provided.",
            )
        try:
            password_hasher.verify(
                hash=user.password_hash,
                password=data.password,
            )
        except VerifyMismatchError as exception:
            raise InvalidInputError(
                message="Invalid credentials provided.",
            ) from exception
        if password_hasher.check_needs_rehash(
            hash=user.password_hash,
        ):
            # update user's password hash
            await self._user_repo.update_user_password(
                user_id=user.id,
                password_hash=password_hasher.hash(
                    password=data.password,
                ),
            )

        # create authentication token
        authentication_token = await self._auth_repo.create_authentication_token(
            user_id=user.id
        )

        # update user's last login timestamp
        await self._user_repo.update_user_last_login(user_id=user.id)

        return LoginUserResult(
            authentication_token=authentication_token,
            user=user,
        )

    async def verify_authentication_token(self, authentication_token: str) -> UUID:
        """
        Verify the given authentication token and
        return the corresponding user ID.
        """
        user_id = await self._auth_repo.get_user_id_from_authentication_token(
            authentication_token=authentication_token,
        )

        if not user_id:
            raise UnauthenticatedError(
                message="Invalid authentication token provided.",
            )
        return user_id

    async def remove_authentication_token(
        self,
        authentication_token: str,
        user_id: UUID,
    ) -> None:
        """Remove the authentication token for the given user ID."""
        await self._auth_repo.remove_authentication_token(
            authentication_token=authentication_token,
            user_id=user_id,
        )

    async def send_password_reset_request(
        self,
        data: PasswordResetRequestInput,
        user_agent: UserAgent,
    ) -> None:
        """Send a password reset request to the given email."""
        existing_user = await self._user_repo.get_user_by_email(email=data.email)
        if existing_user is not None:
            reset_token = await self._auth_repo.create_password_reset_token(
                user_id=existing_user.id,
                last_login_at=existing_user.last_login_at,
            )
            send_password_reset_request_email.delay(
                to=existing_user.email,
                username=existing_user.username,
                password_reset_token=reset_token,
                operating_system=user_agent.get_os(),
                browser_name=user_agent.get_browser(),
            )

    async def reset_password(self, data: PasswordResetInput) -> None:
        """Reset the relevant user's password with the given credentials."""
        reset_token_hash = sha256(data.reset_token.encode()).hexdigest()

        existing_user = await self._user_repo.get_user_by_email(email=data.email)
        password_reset_token = await self._auth_repo.get_password_reset_token(
            reset_token_hash=reset_token_hash
        )

        if not (
            existing_user and password_reset_token and existing_user.email == data.email
        ):
            raise InvalidInputError(
                message="Invalid password reset token or email provided."
            )

        if existing_user.last_login_at > password_reset_token.last_login_at:
            # If the user has logged in again after generating the password
            # reset token, the generated token becomes invalid.
            raise InvalidInputError(
                message="Invalid password reset token or email provided."
            )

        await self._user_repo.update_user_password(
            user_id=existing_user.id,
            password_hash=password_hasher.hash(
                password=data.new_password,
            ),
        )

        # logout user everywhere
        await self._auth_repo.remove_all_authentication_tokens(
            user_id=existing_user.id,
        )
