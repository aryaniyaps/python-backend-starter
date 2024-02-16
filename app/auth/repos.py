from datetime import datetime
from hashlib import sha256
from secrets import token_hex
from uuid import UUID

from geoip2.database import Reader
from redis.asyncio import Redis
from sqlalchemy import ScalarResult, delete, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from user_agents.parsers import UserAgent

from app.auth.models import PasswordResetToken, UserSession
from app.auth.types import UserInfo
from app.core.constants import PASSWORD_RESET_TOKEN_EXPIRES_IN
from app.core.geo_ip import get_ip_location


class UserSessionRepo:
    def __init__(
        self,
        session: AsyncSession,
        geoip_reader: Reader,
    ) -> None:
        self._session = session
        self._geoip_reader = geoip_reader

    async def create_user_session(
        self,
        user_id: UUID,
        ip_address: str,
        user_agent: UserAgent,
    ) -> UserSession:
        """Create a new user session."""
        # TODO: pass device ID here, like instagram does on register/ login
        # TODO: store the GeoID of the region (of a bigger area like a country) along with the location string
        # this can help us detect new logins in a better way
        user_session = UserSession(
            user_id=user_id,
            ip_address=ip_address,
            location=get_ip_location(
                ip_address=ip_address,
                geoip_reader=self._geoip_reader,
            ),
            user_agent=str(user_agent),
        )
        self._session.add(user_session)
        await self._session.commit()
        return user_session

    async def check_user_session_exists(
        self,
        user_id: UUID,
        user_agent: str,
        ip_address: str,
    ) -> bool:
        """Check whether user sessions for the user exist with the given user agent and IP address."""
        # FIXME: dont check IP addresses too strictly, they can be dynamic in some environments
        # TODO: pass device ID here, like instagram does on register/ login
        # TODO: store the GeoID of the region (of a bigger area like a country) along with the location string
        # this can help us detect new logins in a better way
        results = await self._session.scalars(
            select(UserSession).where(
                UserSession.user_id == user_id
                and UserSession.user_agent == user_agent
                and UserSession.ip_address == ip_address
            ),
        )
        return results.first() is not None

    async def check_user_session_exists_after(
        self, user_id: UUID, timestamp: datetime
    ) -> bool:
        """Check whether user sessions for the user which are created after the given timestamp exist."""
        results = await self._session.scalars(
            select(UserSession).where(
                UserSession.user_id == user_id and UserSession.created_at > timestamp
            ),
        )
        return results.first() is not None

    async def get_user_sessions(self, user_id: UUID) -> ScalarResult[UserSession]:
        """Get user sessions for the given user ID."""
        return await self._session.scalars(
            select(UserSession).where(
                UserSession.user_id == user_id,
            ),
        )

    async def delete_user_session(
        self,
        user_session_id: UUID,
        user_id: UUID,
    ) -> None:
        """Delete a user session."""
        await self._session.execute(
            delete(UserSession).where(
                UserSession.id == user_session_id and UserSession.user_id == user_id,
            ),
        )

    async def update_user_session(
        self,
        user_session_id: UUID,
        logged_out_at: datetime | None,
    ) -> None:
        """Delete a user session."""
        await self._session.execute(
            update(UserSession)
            .where(UserSession.id == user_session_id)
            .values(
                logged_out_at=logged_out_at,
            )
        )

    async def logout_user_sessions(
        self,
        user_id: UUID,
    ) -> None:
        """Mark all user sessions with the given user ID as logged out."""
        await self._session.execute(
            update(UserSession)
            .where(UserSession.user_id == user_id)
            .values(
                logged_out_at=text("NOW()"),
            ),
        )


class AuthenticationTokenRepo:
    def __init__(
        self,
        redis_client: Redis,
    ) -> None:
        self._redis_client = redis_client

    async def create_authentication_token(
        self,
        user_id: UUID,
        user_session_id: UUID,
    ) -> str:
        """Create a new authentication token."""
        authentication_token = self.generate_authentication_token()
        # hash authentication token before storing
        authentication_token_hash = self.hash_authentication_token(
            authentication_token=authentication_token,
        )
        await self._redis_client.hset(
            name=self.generate_authentication_token_key(
                authentication_token_hash=authentication_token_hash,
            ),
            mapping={
                "user_id": user_id.bytes,
                "user_session_id": user_session_id.bytes,
            },
        )  # type: ignore[misc]
        await self._redis_client.sadd(
            self.generate_token_owner_key(
                user_id=user_id,
            ),
            authentication_token_hash,
        )  # type: ignore[misc]
        return authentication_token

    @staticmethod
    def generate_authentication_token() -> str:
        """Generate an authentication token."""
        return token_hex(32)

    @staticmethod
    def generate_authentication_token_key(authentication_token_hash: str) -> str:
        """Generate a token key for the authentication token hash."""
        return f"auth-tokens:${authentication_token_hash}"

    @staticmethod
    def generate_token_owner_key(user_id: UUID) -> str:
        """Generate a token owner key for the user ID."""
        return f"auth-token-owners:${user_id}"

    @staticmethod
    def hash_authentication_token(authentication_token: str) -> str:
        """Hash the given authentication token."""
        return sha256(authentication_token.encode()).hexdigest()

    async def get_user_info_for_authentication_token(
        self,
        authentication_token: str,
    ) -> UserInfo | None:
        """Get the user ID and user session ID for the authentication token."""
        user_info = await self._redis_client.hgetall(
            name=self.generate_authentication_token_key(
                authentication_token_hash=self.hash_authentication_token(
                    authentication_token=authentication_token,
                ),
            ),
        )  # type: ignore[misc]
        if user_info is not None:
            return UserInfo(
                user_id=UUID(
                    bytes=user_info.get("user_id"),
                ),
                user_session_id=UUID(
                    bytes=user_info.get("user_session_id"),
                ),
            )
        return None

    async def remove_authentication_token(
        self,
        authentication_token: str,
        user_id: UUID,
    ) -> None:
        """Remove the given authentication token."""
        authentication_token_hash = self.hash_authentication_token(
            authentication_token=authentication_token,
        )
        await self._redis_client.delete(authentication_token_hash)
        await self._redis_client.srem(
            self.generate_token_owner_key(
                user_id=user_id,
            ),
            authentication_token_hash,
        )  # type: ignore[misc]

    async def remove_all_authentication_tokens(
        self,
        user_id: UUID,
    ) -> None:
        """Remove all authentication tokens for the given user ID."""
        authentication_token_hashes = await self._redis_client.smembers(
            name=self.generate_token_owner_key(
                user_id=user_id,
            ),
        )  # type: ignore[misc]
        if authentication_token_hashes:
            await self._redis_client.delete(
                *[
                    self.generate_authentication_token_key(
                        authentication_token_hash=authentication_token_hash,
                    )
                    for authentication_token_hash in authentication_token_hashes
                ]
            )
        await self._redis_client.delete(
            self.generate_token_owner_key(
                user_id=user_id,
            ),
        )


class PasswordResetTokenRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def generate_password_reset_token() -> str:
        """Generate a password reset token."""
        # Generate a random token
        return token_hex(32)

    @staticmethod
    def hash_password_reset_token(password_reset_token: str) -> str:
        """Hash the given password reset token."""
        return sha256(password_reset_token.encode()).hexdigest()

    async def create_password_reset_token(
        self,
        user_id: UUID,
    ) -> str:
        """Create a new password reset token."""
        expires_at = text(
            f"NOW() + INTERVAL '{PASSWORD_RESET_TOKEN_EXPIRES_IN} SECOND'",
        )

        reset_token = self.generate_password_reset_token()

        self._session.add(
            PasswordResetToken(
                user_id=user_id,
                # hash password reset token before storing
                token_hash=self.hash_password_reset_token(
                    password_reset_token=reset_token,
                ),
                expires_at=expires_at,
            ),
        )
        await self._session.commit()
        return reset_token

    async def get_password_reset_token_by_reset_token(
        self,
        reset_token: str,
    ) -> PasswordResetToken | None:
        """Get a password reset token by reset token."""
        return await self._session.scalar(
            select(PasswordResetToken).where(
                PasswordResetToken.token_hash
                == self.hash_password_reset_token(reset_token),
            ),
        )

    async def delete_password_reset_tokens(
        self,
        user_id: UUID,
    ) -> None:
        """Delete password reset tokens for the given user ID."""
        await self._session.execute(
            delete(PasswordResetToken).where(
                PasswordResetToken.user_id == user_id,
            ),
        )
