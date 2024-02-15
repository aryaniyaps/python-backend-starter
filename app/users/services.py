from datetime import UTC, datetime
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from geoip2.database import Reader
from user_agents.parsers import UserAgent

from app.core.errors import InvalidInputError, ResourceNotFoundError
from app.core.geo_ip import get_ip_location
from app.worker import task_queue

from .models import User
from .repos import UserRepo


class UserService:
    def __init__(
        self,
        user_repo: UserRepo,
        password_hasher: PasswordHasher,
        geoip_reader: Reader,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._geoip_reader = geoip_reader

    async def get_user_by_id(self, user_id: UUID) -> User:
        """Get a user by ID."""
        user = await self._user_repo.get_user_by_id(user_id=user_id)
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
            and await self._user_repo.get_user_by_username(
                username=username,
            )
            is not None
        ):
            raise InvalidInputError(
                message="User with that username already exists.",
            )
        return await self._user_repo.update_user(
            user=user,
            username=username,
        )

    async def update_user_password(
        self,
        user_id: UUID,
        new_password: str,
        current_password: str,
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

        return await self._user_repo.update_user(
            user=user,
            password=new_password,
        )

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
            and await self._user_repo.get_user_by_email(
                email=email,
            )
            is not None
        ):
            raise InvalidInputError(
                message="User with that email already exists.",
            )

        verification_token = await self._user_repo.create_email_verification_token(
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
            await self._user_repo.get_email_verification_token_by_token_email(
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

        await self._user_repo.delete_email_verification_tokens(email=email)

        return await self._user_repo.update_user(
            user=user,
            email=email,
        )
