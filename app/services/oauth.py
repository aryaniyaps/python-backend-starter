from datetime import UTC, datetime

import humanize
import nanoid
from fastapi_sso.sso.base import OpenID
from geoip2.database import Reader
from user_agents.parsers import UserAgent

from app.lib.constants import MAX_USERNAME_LENGTH
from app.lib.enums import AuthProviderType
from app.lib.errors import InvalidInputError
from app.lib.geo_ip import get_city_location, get_geoip_city
from app.repositories.auth_provider import AuthProviderRepo
from app.repositories.authentication_token import AuthenticationTokenRepo
from app.repositories.user import UserRepo
from app.repositories.user_session import UserSessionRepo
from app.worker import task_queue


class OAuthService:
    def __init__(
        self,
        user_repo: UserRepo,
        authentication_token_repo: AuthenticationTokenRepo,
        auth_provider_repo: AuthProviderRepo,
        user_session_repo: UserSessionRepo,
        geoip_reader: Reader,
    ) -> None:
        self._user_repo = user_repo
        self._user_session_repo = user_session_repo
        self._authentication_token_repo = authentication_token_repo
        self._auth_provider_repo = auth_provider_repo
        self._geoip_reader = geoip_reader

    async def generate_unique_username(self, display_name: str) -> str:
        """Generate an unique username based on the given display name."""
        base_username = display_name.strip().replace(" ", "_")

        # Truncate if the base username exceeds the maximum length
        if len(base_username) > MAX_USERNAME_LENGTH:
            base_username = base_username[:MAX_USERNAME_LENGTH]

        proposed_username = base_username

        # Check if the proposed username already exists
        while (
            await self._user_repo.get_by_username(
                username=proposed_username,
            )
            is not None
        ):
            # If the proposed username already exists, attach a nanoid to the end and check again
            base_username_truncated = base_username[: MAX_USERNAME_LENGTH - 4]
            proposed_username = f"{base_username_truncated}_{nanoid.generate(size=4)}"

        return proposed_username

    async def login_or_register_user(
        self,
        openid_user: OpenID | None,
        provider: AuthProviderType,
        request_ip: str,
        user_agent: UserAgent,
    ) -> str:
        """Login or register the user associated with the given OpenID credentials."""
        if (
            openid_user is None
            or openid_user.display_name is None
            or openid_user.email is None
        ):
            raise InvalidInputError(
                message="Couldn't sign in user.",
            )

        existing_user = await self._user_repo.get_by_email(
            email=openid_user.email,
        )

        if existing_user is not None:
            # login user here
            if not await self._auth_provider_repo.check_if_exists(
                user_id=existing_user.id,
                provider=provider,
            ):
                # users must explicitly link auth providers before login
                raise InvalidInputError(
                    message="Couldn't sign in with the given provider.",
                )
            if not await self._user_session_repo.check_if_device_exists(
                user_id=existing_user.id,
                device=user_agent.device,
            ):
                await task_queue.enqueue(
                    "send_new_login_device_detected_email",
                    receiver=existing_user.email,
                    username=existing_user.username,
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
                user_id=existing_user.id,
                ip_address=request_ip,
                user_agent=user_agent,
            )

            # create authentication token
            return await self._authentication_token_repo.create(
                user_id=existing_user.id,
                user_session_id=user_session.id,
            )

        username = await self.generate_unique_username(
            display_name=openid_user.display_name,
        )

        user = await self._user_repo.create(
            username=username,
            email=openid_user.email,
        )

        await self._auth_provider_repo.create(
            user_id=user.id,
            provider=provider,
        )

        user_session = await self._user_session_repo.create(
            user_id=user.id,
            ip_address=request_ip,
            user_agent=user_agent,
        )

        authentication_token = await self._authentication_token_repo.create(
            user_id=user.id,
            user_session_id=user_session.id,
        )

        await task_queue.enqueue(
            "send_onboarding_email",
            receiver=user.email,
            username=user.username,
        )

        return authentication_token
