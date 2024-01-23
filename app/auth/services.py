from datetime import UTC, datetime
from hashlib import sha256
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import HashingError, VerifyMismatchError
from user_agents.parsers import UserAgent

from app.auth.repos import AuthRepo
from app.auth.tasks import (
    send_new_login_location_detected_email,
    send_onboarding_email,
    send_password_reset_request_email,
)
from app.core.errors import InvalidInputError, UnauthenticatedError, UnexpectedError
from app.users.models import User
from app.users.repos import UserRepo
from app.worker import task_queue


class AuthService:
    def __init__(
        self,
        auth_repo: AuthRepo,
        user_repo: UserRepo,
        password_hasher: PasswordHasher,
    ) -> None:
        self._auth_repo = auth_repo
        self._user_repo = user_repo
        self._password_hasher = password_hasher

    async def register_user(
        self,
        email: str,
        username: str,
        password: str,
        request_ip: str,
    ) -> tuple[str, User]:
        """Register a new user."""
        try:
            if (
                await self._user_repo.get_user_by_email(
                    email=email,
                )
                is not None
            ):
                raise InvalidInputError(
                    message="User with that email already exists.",
                )
            if (
                await self._user_repo.get_user_by_username(
                    username=username,
                )
                is not None
            ):
                raise InvalidInputError(
                    message="User with that username already exists.",
                )
            user = await self._user_repo.create_user(
                username=username,
                email=email,
                password=password,
                login_ip=request_ip,
            )
        except HashingError as exception:
            raise UnexpectedError(
                message="Could not create user. Please try again.",
            ) from exception

        authentication_token = await self._auth_repo.create_authentication_token(
            user_id=user.id,
        )

        task_queue.enqueue(
            send_onboarding_email,
            receiver=user.email,
            username=user.username,
        )

        return authentication_token, user

    async def login_user(
        self,
        login: str,
        password: str,
        user_agent: UserAgent,
        request_ip: str,
    ) -> tuple[str, User]:
        """Check the given credentials and return the relevant user if they are valid."""
        if "@" in login:
            # if "@" is present, assume it's an email
            user = await self._user_repo.get_user_by_email(
                email=login,
            )
        else:
            # assume it's an username
            user = await self._user_repo.get_user_by_username(
                username=login,
            )
        if not user:
            raise InvalidInputError(
                message="Invalid credentials provided.",
            )
        try:
            self._password_hasher.verify(
                hash=user.password_hash,
                password=password,
            )
        except VerifyMismatchError as exception:
            raise InvalidInputError(
                message="Invalid credentials provided.",
            ) from exception

        # create authentication token
        authentication_token = await self._auth_repo.create_authentication_token(
            user_id=user.id,
        )

        previous_login_ip = user.last_login_ip

        if self._password_hasher.check_needs_rehash(
            hash=user.password_hash,
        ):
            # update user's password hash, last login timestamp and login IP
            user = await self._user_repo.update_user(
                user=user,
                password=password,
                last_login_ip=request_ip,
                update_last_login=True,
            )
        else:
            # update user's last login timestamp and login IP
            user = await self._user_repo.update_user(
                user=user,
                last_login_ip=request_ip,
                update_last_login=True,
            )

        if previous_login_ip != request_ip:
            task_queue.enqueue(
                send_new_login_location_detected_email,
                receiver=user.email,
                username=user.username,
                login_timestamp=user.last_login_at,
                device=user_agent.get_device(),
                browser_name=user_agent.get_browser(),
                # TODO: pass information about where this request took place from the IP address.
                location="",
                ip_address=request_ip,
            )

        return authentication_token, user

    async def verify_authentication_token(self, authentication_token: str) -> UUID:
        """Verify the given authentication token and return the corresponding user ID."""
        # TODO: return the login session ID along with the user ID here
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
        email: str,
        user_agent: UserAgent,
        request_ip: str,
    ) -> None:
        """Send a password reset request to the given email."""
        existing_user = await self._user_repo.get_user_by_email(email=email)
        if existing_user is not None:
            reset_token = await self._auth_repo.create_password_reset_token(
                user_id=existing_user.id,
                last_login_at=existing_user.last_login_at,
            )

            task_queue.enqueue(
                send_password_reset_request_email,
                receiver=existing_user.email,
                username=existing_user.username,
                password_reset_token=reset_token,
                device=user_agent.get_device(),
                browser_name=user_agent.get_browser(),
                # TODO: pass information about where this request took place from the IP address.
                location="",
                ip_address=request_ip,
            )

    async def reset_password(
        self,
        email: str,
        reset_token: str,
        new_password: str,
    ) -> None:
        """Reset the relevant user's password with the given credentials."""
        reset_token_hash = sha256(reset_token.encode()).hexdigest()

        existing_user = await self._user_repo.get_user_by_email(email=email)
        password_reset_token = await self._auth_repo.get_password_reset_token(
            reset_token_hash=reset_token_hash,
        )

        if not (
            existing_user and password_reset_token and existing_user.email == email
        ):
            raise InvalidInputError(
                message="Invalid password reset token or email provided.",
            )

        if datetime.now(UTC) > password_reset_token.expires_at:
            # password reset token has expired.
            raise InvalidInputError(
                message="Invalid password reset token or email provided.",
            )

        if existing_user.last_login_at > password_reset_token.last_login_at:
            # If the user has logged in again after generating the password
            # reset token, the generated token becomes invalid.
            raise InvalidInputError(
                message="Invalid password reset token or email provided.",
            )

        await self._user_repo.update_user(
            user=existing_user,
            password=new_password,
        )

        # logout user everywhere
        await self._auth_repo.remove_all_authentication_tokens(
            user_id=existing_user.id,
        )
