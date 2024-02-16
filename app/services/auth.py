from datetime import UTC, datetime
from uuid import UUID

import humanize
from argon2 import PasswordHasher
from argon2.exceptions import HashingError, VerifyMismatchError
from geoip2.database import Reader
from sqlalchemy import ScalarResult
from user_agents.parsers import UserAgent

from app.auth.types import UserInfo
from app.core.errors import InvalidInputError, UnauthenticatedError, UnexpectedError
from app.core.geo_ip import get_ip_location
from app.core.security import check_password_strength
from app.models.user import User
from app.models.user_session import UserSession
from app.repositories.authentication_token import AuthenticationTokenRepo
from app.repositories.email_verification_token import EmailVerificationTokenRepo
from app.repositories.password_reset_token import PasswordResetTokenRepo
from app.repositories.user import UserRepo
from app.repositories.user_session import UserSessionRepo
from app.worker import task_queue


class AuthService:
    def __init__(
        self,
        user_session_repo: UserSessionRepo,
        password_reset_token_repo: PasswordResetTokenRepo,
        authentication_token_repo: AuthenticationTokenRepo,
        user_repo: UserRepo,
        email_verification_token_repo: EmailVerificationTokenRepo,
        password_hasher: PasswordHasher,
        geoip_reader: Reader,
    ) -> None:
        self._user_session_repo = user_session_repo
        self._password_reset_token_repo = password_reset_token_repo
        self._authentication_token_repo = authentication_token_repo
        self._user_repo = user_repo
        self._email_verification_token_repo = email_verification_token_repo
        self._password_hasher = password_hasher
        self._geoip_reader = geoip_reader

    async def send_email_verification_request(
        self,
        email: str,
        user_agent: UserAgent,
        request_ip: str,
    ) -> None:
        """Send an email verification request to the given email."""
        if (
            await self._user_repo.get_by_email(
                email=email,
            )
            is not None
        ):
            raise InvalidInputError(
                message="User with that email already exists.",
            )

        verification_token = (
            await self._email_verification_token_repo.create(
                email=email,
            )
        )

        # send verification request email
        await task_queue.enqueue(
            "send_email_verification_request_email",
            receiver=email,
            verification_token=verification_token,
            device=user_agent.get_device(),
            browser_name=user_agent.get_browser(),
            location=get_ip_location(
                ip_address=request_ip,
                geoip_reader=self._geoip_reader,
            ),
            ip_address=request_ip,
        )

    async def register_user(
        self,
        email: str,
        email_verification_token: str,
        username: str,
        password: str,
        request_ip: str,
        user_agent: UserAgent,
    ) -> tuple[str, User]:
        """Register a new user."""
        if not check_password_strength(
            password=password,
            context={
                "username": username,
                "email": email,
            },
        ):
            raise InvalidInputError(
                message="Enter a stronger password.",
            )
        try:
            if (
                await self._user_repo.get_by_username(
                    username=username,
                )
                is not None
            ):
                raise InvalidInputError(
                    message="User with that username already exists.",
                )

            verification_token = await self._email_verification_token_repo.get_by_token_email(
                verification_token=email_verification_token,
                email=email,
            )

            if (
                verification_token is None
                or datetime.now(UTC) > verification_token.expires_at
            ):
                raise InvalidInputError(
                    message="Invalid email or email verification token provided."
                )

            await self._email_verification_token_repo.delete_all(
                email=email
            )

            user = await self._user_repo.create(
                username=username,
                email=email,
                password=password,
            )

            user_session = await self._user_session_repo.create(
                user_id=user.id,
                ip_address=request_ip,
                user_agent=user_agent,
            )
        except HashingError as exception:
            raise UnexpectedError(
                message="Could not create user. Please try again.",
            ) from exception

        authentication_token = await self._authentication_token_repo.create(
            user_id=user.id,
            user_session_id=user_session.id,
        )
        await task_queue.enqueue(
            "send_onboarding_email",
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
        """
        Login a user.

        Check the given credentials and return the relevant authentication
        token and user and if they are valid.
        """
        if "@" in login:
            # if "@" is present, assume it's an email
            user = await self._user_repo.get_by_email(
                email=login,
            )
        else:
            # assume it's an username
            user = await self._user_repo.get_by_username(
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

        if not await self._user_session_repo.check_if_exists(
            user_id=user.id,
            user_agent=str(user_agent),
            ip_address=request_ip,
        ):
            # FIXME: maybe send emails only when new device is detected, and not login location.
            # send the IP address as metadata alone.
            await task_queue.enqueue(
                "send_new_login_location_detected_email",
                receiver=user.email,
                username=user.username,
                login_timestamp=humanize.naturaldate(datetime.now(UTC)),
                device=user_agent.get_device(),
                browser_name=user_agent.get_browser(),
                location=get_ip_location(
                    ip_address=request_ip,
                    geoip_reader=self._geoip_reader,
                ),
                ip_address=request_ip,
            )

        user_session = await self._user_session_repo.create(
            user_id=user.id,
            ip_address=request_ip,
            user_agent=user_agent,
        )

        # create authentication token
        authentication_token = await self._authentication_token_repo.create(
            user_id=user.id,
            user_session_id=user_session.id,
        )

        if self._password_hasher.check_needs_rehash(
            hash=user.password_hash,
        ):
            # update user's password hash
            user = await self._user_repo.update(
                user=user,
                password=password,
            )

        return authentication_token, user

    async def get_user_sessions(self, user_id: UUID) -> ScalarResult[UserSession]:
        """Get user sessions for the given user ID."""
        return await self._user_session_repo.get_all(
            user_id=user_id,
        )

    async def logout_user(
        self,
        authentication_token: str,
        user_session_id: UUID,
        user_id: UUID,
        *,
        remember_session: bool,
    ) -> None:
        """Logout the user."""
        await self._authentication_token_repo.delete(
            authentication_token=authentication_token,
            user_id=user_id,
        )
        if not remember_session:
            return await self._user_session_repo.delete(
                user_session_id=user_session_id,
                user_id=user_id,
            )
        return await self._user_session_repo.update(
            user_session_id=user_session_id,
            logged_out_at=datetime.now(UTC),
        )

    async def get_user_info_for_authentication_token(
        self, authentication_token: str
    ) -> UserInfo:
        """Verify the given authentication token and return the corresponding user info."""
        user_info = await self._authentication_token_repo.get_user_info(
            authentication_token=authentication_token,
        )

        if not user_info:
            raise UnauthenticatedError(
                message="Invalid authentication token provided.",
            )
        return user_info

    async def send_password_reset_request(
        self,
        email: str,
        user_agent: UserAgent,
        request_ip: str,
    ) -> None:
        """Send a password reset request to the given user if they exist."""
        existing_user = await self._user_repo.get_by_email(email=email)
        if existing_user is not None:
            reset_token = await self._password_reset_token_repo.create(
                user_id=existing_user.id,
            )
            await task_queue.enqueue(
                "send_password_reset_request_email",
                receiver=existing_user.email,
                username=existing_user.username,
                password_reset_token=reset_token,
                device=user_agent.get_device(),
                browser_name=user_agent.get_browser(),
                location=get_ip_location(
                    ip_address=request_ip,
                    geoip_reader=self._geoip_reader,
                ),
                ip_address=request_ip,
            )

    async def reset_password(
        self,
        email: str,
        reset_token: str,
        new_password: str,
        request_ip: str,
        user_agent: UserAgent,
    ) -> None:
        """Reset the relevant user's password with the given credentials."""
        existing_user = await self._user_repo.get_by_email(email=email)
        password_reset_token = await self._password_reset_token_repo.get_by_reset_token(
            reset_token=reset_token,
        )

        if not (existing_user and password_reset_token):
            raise InvalidInputError(
                message="Invalid password reset token or email provided.",
            )

        if datetime.now(UTC) > password_reset_token.expires_at:
            # password reset token has expired.
            raise InvalidInputError(
                message="Invalid password reset token or email provided.",
            )

        if not check_password_strength(
            password=new_password,
            context={
                "username": existing_user.username,
                "email": existing_user.email,
            },
        ):
            raise InvalidInputError(
                message="Enter a stronger password.",
            )

        # delete all password reset tokens to prevent duplicate use
        await self._password_reset_token_repo.delete_all(
            user_id=existing_user.id,
        )

        if await self._user_session_repo.check_if_exists_after(
            user_id=existing_user.id,
            timestamp=password_reset_token.created_at,
        ):
            # If the user has logged in again after generating the password
            # reset token, the generated token becomes invalid.
            # TODO: review logic here
            raise InvalidInputError(
                message="Invalid password reset token or email provided.",
            )

        await self._user_repo.update(
            user=existing_user,
            password=new_password,
        )

        # logout user everywhere
        await self._authentication_token_repo.delete_all(
            user_id=existing_user.id,
        )

        await self._user_session_repo.logout_all(
            user_id=existing_user.id,
        )

        # send password reset mail
        await task_queue.enqueue(
            "send_password_reset_email",
            receiver=existing_user.email,
            username=existing_user.username,
            device=user_agent.get_device(),
            browser_name=user_agent.get_browser(),
            location=get_ip_location(
                ip_address=request_ip,
                geoip_reader=self._geoip_reader,
            ),
            ip_address=request_ip,
        )
