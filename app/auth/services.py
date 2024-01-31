from datetime import UTC, datetime
from hashlib import sha256
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import HashingError, VerifyMismatchError
from geoip2.database import Reader
from sqlalchemy import ScalarResult
from user_agents.parsers import UserAgent

from app.auth.models import LoginSession
from app.auth.repos import AuthRepo
from app.auth.tasks import (
    send_new_login_location_detected_email,
    send_onboarding_email,
    send_password_reset_request_email,
)
from app.core.errors import InvalidInputError, UnauthenticatedError, UnexpectedError
from app.core.geo_ip import format_city_location
from app.users.models import User
from app.users.repos import UserRepo
from app.worker import task_queue


class AuthService:
    def __init__(
        self,
        auth_repo: AuthRepo,
        user_repo: UserRepo,
        password_hasher: PasswordHasher,
        geoip_reader: Reader,
    ) -> None:
        self._auth_repo = auth_repo
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._geoip_reader = geoip_reader

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
            )

            login_session = await self._auth_repo.create_login_session(
                user_id=user.id,
                ip_address=request_ip,
            )
        except HashingError as exception:
            raise UnexpectedError(
                message="Could not create user. Please try again.",
            ) from exception

        authentication_token = await self._auth_repo.create_authentication_token(
            user_id=user.id,
            login_session_id=login_session.id,
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
        """Check the given credentials and return the relevant authentication token and user and if they are valid."""
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

        # TODO: (check if login session already exists with IP address?)
        # This can happen in scenarios where user logs in, (via api), forgets password
        # and also forgets to logout. so the session wont be deleted.

        # solution: Login sessions need to be persisted across logins for devices (only then we can notify on new logins)
        # upon each login, the last_login_at alone needs to change

        # when users logout we delete the authentication tokens
        # we should also set a flag like `is_logged_out` = True on the login session
        login_session = await self._auth_repo.create_login_session(
            user_id=user.id,
            ip_address=request_ip,
        )

        # create authentication token
        authentication_token = await self._auth_repo.create_authentication_token(
            user_id=user.id,
            login_session_id=login_session.id,
        )

        previous_login_ip = user.last_login_ip

        if self._password_hasher.check_needs_rehash(
            hash=user.password_hash,
        ):
            # update user's password hash
            user = await self._user_repo.update_user(
                user=user,
                password=password,
            )

        city = self._geoip_reader.city(request_ip)

        if previous_login_ip != request_ip:
            # TODO: send new login detected based on the device, and not the IP address
            task_queue.enqueue(
                send_new_login_location_detected_email,
                receiver=user.email,
                username=user.username,
                login_timestamp=login_session.created_at,
                device=user_agent.get_device(),
                browser_name=user_agent.get_browser(),
                location=format_city_location(city),
                ip_address=request_ip,
            )

        return authentication_token, user

    async def get_login_sessions(self, user_id: UUID) -> ScalarResult[LoginSession]:
        """Get login sessions for the given user ID."""
        return await self._auth_repo.get_login_sessions(
            user_id=user_id,
        )

    async def delete_login_session(self, login_session_id: UUID, user_id: UUID) -> None:
        """Delete a login session."""
        await self._auth_repo.delete_login_session(
            login_session_id=login_session_id,
            user_id=user_id,
        )

    async def delete_login_sessions(
        self,
        user_id: UUID,
        except_login_session_id: UUID,
    ) -> None:
        """Delete all login sessions for the user except for the given login session ID."""
        await self._auth_repo.delete_login_sessions(
            except_login_session_id=except_login_session_id,
            user_id=user_id,
        )

    async def verify_authentication_token(
        self, authentication_token: str
    ) -> tuple[UUID, UUID]:
        """Verify the given authentication token and return the corresponding user ID."""
        user_info = await self._auth_repo.get_user_info_for_authentication_token(
            authentication_token=authentication_token,
        )

        if not user_info:
            raise UnauthenticatedError(
                message="Invalid authentication token provided.",
            )
        return user_info

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
            )

            city = self._geoip_reader.city(request_ip)

            task_queue.enqueue(
                send_password_reset_request_email,
                receiver=existing_user.email,
                username=existing_user.username,
                password_reset_token=reset_token,
                device=user_agent.get_device(),
                browser_name=user_agent.get_browser(),
                location=format_city_location(city),
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

        if existing_user.last_login_at > password_reset_token.created_at:
            # If the user has logged in again after generating the password
            # reset token, the generated token becomes invalid.
            raise InvalidInputError(
                message="Invalid password reset token or email provided.",
            )

        await self._user_repo.update_user(
            user=existing_user,
            password=new_password,
        )

        # delete all other password reset tokens for user
        await self._auth_repo.delete_password_reset_tokens(
            user_id=existing_user.id,
        )

        # logout user everywhere
        await self._auth_repo.remove_all_authentication_tokens(
            user_id=existing_user.id,
        )
