from datetime import UTC, datetime
from uuid import UUID

from geoip2.database import Reader
from user_agents.parsers import UserAgent

from app.lib.errors import InvalidInputError, ResourceNotFoundError
from app.lib.geo_ip import get_city_location, get_geoip_city
from app.models.user import User
from app.repositories.authentication_token import AuthenticationTokenRepo
from app.repositories.email_verification_code import EmailVerificationCodeRepo
from app.repositories.user import UserRepo
from app.repositories.user_session import UserSessionRepo
from app.worker import task_queue


class UserService:
    def __init__(
        self,
        user_repo: UserRepo,
        email_verification_code_repo: EmailVerificationCodeRepo,
        authentication_token_repo: AuthenticationTokenRepo,
        user_session_repo: UserSessionRepo,
        geoip_reader: Reader,
    ) -> None:
        self._user_repo = user_repo
        self._email_verification_code_repo = email_verification_code_repo
        self._authentication_token_repo = authentication_token_repo
        self._user_session_repo = user_session_repo
        self._geoip_reader = geoip_reader

    async def get_user_by_id(self, *, user_id: UUID) -> User:
        """Get a user by ID."""
        user = await self._user_repo.get(user_id=user_id)
        if user is None:
            raise ResourceNotFoundError(
                message="Couldn't find user with the given ID.",
            )
        return user

    async def update_user(
        self,
        *,
        user_id: UUID,
        display_name: str | None = None,
    ) -> User:
        """Update the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)
        return await self._user_repo.update(
            user=user,
            display_name=display_name,
        )

    async def send_change_email_request(
        self,
        *,
        user_id: UUID,
        email: str,
        current_password: str,
        user_agent: UserAgent,
        request_ip: str,
    ) -> None:
        """Update the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)

        # TODO: reauthenticate here using webauthn

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

        verification_code = await self._email_verification_code_repo.create(email=email)

        # send verification request email
        await task_queue.enqueue(
            "send_email_verification_request_email",
            receiver=email,
            verification_code=verification_code,
            device=user_agent.get_device(),
            browser_name=user_agent.get_browser(),
            location=get_city_location(
                city=get_geoip_city(
                    ip_address=request_ip,
                    geoip_reader=self._geoip_reader,
                ),
            ),
            ip_address=request_ip,
        )

    async def update_user_email(
        self,
        *,
        user_id: UUID,
        email: str,
        verification_code: str,
    ) -> User:
        """Update the email for the given user."""
        user = await self.get_user_by_id(user_id=user_id)

        email_verification_code = await self._email_verification_code_repo.get(
            verification_code=verification_code,
            email=email,
        )

        if (
            email_verification_code is None
            or datetime.now(UTC) > email_verification_code.expires_at
        ):
            raise InvalidInputError(
                message="Invalid email or email verification code provided."
            )

        await self._email_verification_code_repo.delete_all(email=email)

        return await self._user_repo.update(
            user=user,
            email=email,
        )
