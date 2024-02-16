from datetime import UTC, datetime
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from geoip2.database import Reader
from user_agents.parsers import UserAgent

from app.lib.errors import InvalidInputError, ResourceNotFoundError
from app.lib.geo_ip import get_ip_location
from app.lib.security import check_password_strength
from app.models.user import User
from app.repositories.authentication_token import AuthenticationTokenRepo
from app.repositories.email_verification_token import EmailVerificationTokenRepo
from app.repositories.user import UserRepo
from app.repositories.user_session import UserSessionRepo
from app.worker import task_queue


class UserService:
    def __init__(
        self,
        user_repo: UserRepo,
        email_verification_token_repo: EmailVerificationTokenRepo,
        authentication_token_repo: AuthenticationTokenRepo,
        user_session_repo: UserSessionRepo,
        password_hasher: PasswordHasher,
        geoip_reader: Reader,
    ) -> None:
        self._user_repo = user_repo
        self._email_verification_token_repo = email_verification_token_repo
        self._authentication_token_repo = authentication_token_repo
        self._user_session_repo = user_session_repo
        self._password_hasher = password_hasher
        self._geoip_reader = geoip_reader

    async def get_user_by_id(self, user_id: UUID) -> User:
        """Get a user by ID."""
        user = await self._user_repo.get(user_id=user_id)
        if user is None:
            raise ResourceNotFoundError(
                message="Couldn't find user with the given ID.",
            )
        return user

    async def update_user(
        self,
        user_id: UUID,
        username: str | None = None,
    ) -> User:
        """Update the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)
        if (
            username
            and await self._user_repo.get_by_username(
                username=username,
            )
            is not None
        ):
            raise InvalidInputError(
                message="User with that username already exists.",
            )
        return await self._user_repo.update(
            user=user,
            username=username,
        )

    async def update_user_password(
        self,
        user_id: UUID,
        new_password: str,
        current_password: str,
        user_agent: UserAgent,
        request_ip: str,
    ) -> User:
        """Update the password for the given user."""
        user = await self.get_user_by_id(user_id=user_id)

        try:
            self._password_hasher.verify(
                hash=user.password_hash,
                password=current_password,
            )
        except VerifyMismatchError as exception:
            raise InvalidInputError(
                message="Invalid current password provided.",
            ) from exception

        if not check_password_strength(
            password=new_password,
            context={
                "username": user.username,
                "email": user.email,
            },
        ):
            raise InvalidInputError(
                message="Enter a stronger password.",
            )

        await self._user_repo.update(
            user=user,
            password=new_password,
        )

        # logout user everywhere
        await self._authentication_token_repo.delete_all(
            user_id=user.id,
        )

        await self._user_session_repo.logout_all(
            user_id=user.id,
        )

        # send password changed mail
        # TODO: maybe rename `reset` to `changed` here
        await task_queue.enqueue(
            "send_password_reset_email",
            receiver=user.email,
            username=user.username,
            device=user_agent.get_device(),
            browser_name=user_agent.get_browser(),
            location=get_ip_location(
                ip_address=request_ip,
                geoip_reader=self._geoip_reader,
            ),
            ip_address=request_ip,
        )

        return user

    async def send_change_email_request(
        self,
        user_id: UUID,
        email: str,
        current_password: str,
        user_agent: UserAgent,
        request_ip: str,
    ) -> None:
        """Update the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)

        try:
            self._password_hasher.verify(
                hash=user.password_hash,
                password=current_password,
            )
        except VerifyMismatchError as exception:
            raise InvalidInputError(
                message="Invalid current password provided.",
            ) from exception

        if (
            email
            and await self._user_repo.get_by_email(
                email=email,
            )
            is not None
        ):
            raise InvalidInputError(
                message="User with that email already exists.",
            )

        verification_token = await self._email_verification_token_repo.create(
            email=email
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

    async def update_user_email(
        self,
        user_id: UUID,
        email: str,
        email_verification_token: str,
    ) -> User:
        """Update the email for the given user."""
        user = await self.get_user_by_id(user_id=user_id)

        verification_token = (
            await self._email_verification_token_repo.get_by_token_email(
                verification_token=email_verification_token,
                email=email,
            )
        )

        if (
            verification_token is None
            or datetime.now(UTC) > verification_token.expires_at
        ):
            raise InvalidInputError(
                message="Invalid email or email verification token provided."
            )

        await self._email_verification_token_repo.delete_all(email=email)

        return await self._user_repo.update(
            user=user,
            email=email,
        )
