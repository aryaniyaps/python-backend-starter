from datetime import UTC, datetime
from uuid import UUID

import humanize
from argon2 import PasswordHasher
from argon2.exceptions import HashingError, VerifyMismatchError
from geoip2.database import Reader
from sqlalchemy import ScalarResult
from user_agents.parsers import UserAgent

from app.lib.enums import AuthProviderType
from app.lib.errors import InvalidInputError, UnauthenticatedError, UnexpectedError
from app.lib.geo_ip import get_city_location, get_geoip_city
from app.lib.security import check_password_strength
from app.models.user import User
from app.models.user_session import UserSession
from app.repositories.auth_provider import AuthProviderRepo
from app.repositories.authentication_token import AuthenticationTokenRepo
from app.repositories.email_verification_code import EmailVerificationCodeRepo
from app.repositories.password_reset_code import PasswordResetCodeRepo
from app.repositories.user import UserRepo
from app.repositories.user_password import UserPasswordRepo
from app.repositories.user_session import UserSessionRepo
from app.types.auth import UserInfo
from app.worker import task_queue


class AuthService:
    def __init__(
        self,
        user_session_repo: UserSessionRepo,
        password_reset_code_repo: PasswordResetCodeRepo,
        authentication_token_repo: AuthenticationTokenRepo,
        auth_provider_repo: AuthProviderRepo,
        user_repo: UserRepo,
        user_password_repo: UserPasswordRepo,
        email_verification_code_repo: EmailVerificationCodeRepo,
        password_hasher: PasswordHasher,
        geoip_reader: Reader,
    ) -> None:
        self._user_session_repo = user_session_repo
        self._password_reset_code_repo = password_reset_code_repo
        self._authentication_token_repo = authentication_token_repo
        self._auth_provider_repo = auth_provider_repo
        self._user_repo = user_repo
        self._user_password_repo = user_password_repo
        self._email_verification_code_repo = email_verification_code_repo
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

        verification_token = await self._email_verification_code_repo.create(
            email=email,
        )

        # send verification request email
        await task_queue.enqueue(
            "send_email_verification_request_email",
            receiver=email,
            verification_token=verification_token,
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

    async def register_user(
        self,
        email: str,
        email_verification_code: str,
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

            verification_code = (
                await self._email_verification_code_repo.get_by_code_email(
                    verification_code=email_verification_code,
                    email=email,
                )
            )

            if (
                verification_code is None
                or datetime.now(UTC) > verification_code.expires_at
            ):
                raise InvalidInputError(
                    message="Invalid email or email verification code provided."
                )

            await self._email_verification_code_repo.delete_all(email=email)

            user = await self._user_repo.create(
                username=username,
                email=email,
            )

            await self._auth_provider_repo.create(
                user_id=user.id,
                provider=AuthProviderType.email_password,
            )

            await self._user_password_repo.create(
                user_id=user.id,
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

        if user is None:
            raise InvalidInputError(
                message="Invalid credentials provided.",
            )

        user_password = await self._user_password_repo.get(user_id=user.id)

        if user_password is None:
            # user must have registered with an oauth provider
            raise InvalidInputError(
                message="Cannot login user with email and password.",
            )

        try:
            self._password_hasher.verify(
                hash=user_password.hash,
                password=password,
            )
        except VerifyMismatchError as exception:
            raise InvalidInputError(
                message="Invalid credentials provided.",
            ) from exception

        if not await self._user_session_repo.check_if_device_exists(
            user_id=user.id,
            device=user_agent.device,
        ):
            await task_queue.enqueue(
                "send_new_login_device_detected_email",
                receiver=user.email,
                username=user.username,
                login_timestamp=humanize.naturaldate(datetime.now(UTC)),
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
            hash=user_password.hash,
        ):
            # update user's password hash
            await self._user_password_repo.update(
                user_password=user_password,
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
            reset_token = await self._password_reset_code_repo.create(
                user_id=existing_user.id,
            )
            await task_queue.enqueue(
                "send_password_reset_request_email",
                receiver=existing_user.email,
                username=existing_user.username,
                password_reset_token=reset_token,
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

    async def reset_password(
        self,
        email: str,
        reset_code: str,
        new_password: str,
        request_ip: str,
        user_agent: UserAgent,
    ) -> None:
        """Reset the relevant user's password with the given credentials."""
        existing_user = await self._user_repo.get_by_email(email=email)
        password_reset_token = await self._password_reset_code_repo.get_by_reset_code(
            reset_code=reset_code,
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
        await self._password_reset_code_repo.delete_all(
            user_id=existing_user.id,
        )

        user_password = await self._user_password_repo.get(
            user_id=existing_user.id,
        )

        if user_password is None:
            # user must have registered with an oauth provider
            await self._user_password_repo.create(
                user_id=existing_user.id,
                password=new_password,
            )
        else:
            await self._user_password_repo.update(
                user_password=user_password,
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
            location=get_city_location(
                city=get_geoip_city(
                    ip_address=request_ip,
                    geoip_reader=self._geoip_reader,
                ),
            ),
            ip_address=request_ip,
        )
