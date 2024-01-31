from datetime import datetime
from hashlib import sha256
from secrets import token_hex
from uuid import UUID

from geoip2.database import Reader
from redis.asyncio import Redis
from sqlalchemy import ScalarResult, delete, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from user_agents.parsers import UserAgent

from app.auth.models import LoginSession, PasswordResetToken
from app.core.constants import PASSWORD_RESET_TOKEN_EXPIRES_IN
from app.core.geo_ip import format_geoip_city


class AuthRepo:
    def __init__(
        self,
        session: AsyncSession,
        redis_client: Redis,
        geoip_reader: Reader,
    ) -> None:
        self._session = session
        self._redis_client = redis_client
        self._geoip_reader = geoip_reader

    async def create_login_session(
        self,
        user_id: UUID,
        ip_address: str,
        user_agent: UserAgent,
    ) -> LoginSession:
        """Create a new login session."""
        city = self._geoip_reader.city(ip_address)
        login_session = LoginSession(
            user_id=user_id,
            ip_address=ip_address,
            location=format_geoip_city(city),
            user_agent=str(user_agent),
        )
        self._session.add(login_session)
        await self._session.commit()
        return login_session

    async def get_login_session(
        self,
        user_id: UUID,
        ip_address: str,
    ) -> LoginSession | None:
        """Get a login session with the given user ID and IP address."""
        # TODO: include user agent to fetch session here?
        return await self._session.scalar(
            select(LoginSession).where(
                LoginSession.user_id == user_id
                and LoginSession.ip_address == ip_address
            ),
        )

    async def check_login_session_exists(
        self,
        user_id: UUID,
        user_agent: str,
        ip_address: str,
    ) -> bool:
        """Check whether login sessions for the user exist with the given user agent and IP address."""
        results = await self._session.scalars(
            select(LoginSession).where(
                LoginSession.user_id == user_id
                and LoginSession.user_agent == user_agent
                and LoginSession.ip_address == ip_address
            ),
        )
        return results.first() is not None

    async def check_login_session_exists_after(
        self, user_id: UUID, timestamp: datetime
    ) -> bool:
        """Check whether login sessions for the user which are created after the given timestamp exist."""
        results = await self._session.scalars(
            select(LoginSession).where(
                LoginSession.user_id == user_id and LoginSession.created_at > timestamp
            ),
        )
        return results.first() is not None

    async def get_login_sessions(self, user_id: UUID) -> ScalarResult[LoginSession]:
        """Get login sessions for the given user ID."""
        return await self._session.scalars(
            select(LoginSession).where(
                LoginSession.user_id == user_id,
            ),
        )

    async def delete_login_session(
        self,
        login_session_id: UUID,
        user_id: UUID,
    ) -> None:
        """Delete a login session."""
        await self._session.execute(
            delete(LoginSession).where(
                LoginSession.id == login_session_id and LoginSession.user_id == user_id,
            ),
        )

    async def update_login_session(
        self,
        login_session_id: UUID,
        logged_out_at: datetime | None,
    ) -> None:
        """Delete a login session."""
        await self._session.execute(
            update(LoginSession)
            .where(LoginSession.id == login_session_id)
            .values(
                logged_out_at=logged_out_at,
            )
        )

    async def delete_login_sessions(
        self,
        user_id: UUID,
        except_login_session_id: UUID,
    ) -> None:
        """Delete all login sessions for the user except for the given login session ID."""
        await self._session.execute(
            delete(LoginSession).where(
                LoginSession.user_id == user_id
                and LoginSession.id != except_login_session_id
            ),
        )

    async def create_authentication_token(
        self,
        user_id: UUID,
        login_session_id: UUID,
    ) -> str:
        """Create a new authentication token."""
        authentication_token = self.generate_authentication_token()
        # hash authentication token before storing
        authentication_token_hash = self.hash_authentication_token(
            authentication_token=authentication_token,
        )
        await self._redis_client.hset(
            name="auth_tokens",
            key=self.generate_authentication_token_key(
                authentication_token_hash=authentication_token_hash,
            ),
            mapping={
                "user_id": user_id.bytes,
                "login_session_id": login_session_id,
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
        # Generate a random token
        return token_hex(32)

    @staticmethod
    def generate_authentication_token_key(authentication_token_hash: str) -> str:
        """Generate a key for the authentication token's hash."""
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
    ) -> tuple[UUID, UUID] | None:
        """Get the user ID and login session ID for the authentication token."""
        user_info = await self._redis_client.hmget(
            name=self.generate_authentication_token_key(
                authentication_token_hash=self.hash_authentication_token(
                    authentication_token=authentication_token,
                ),
            ),
            keys=[
                "user_id",
                "login_session_id",
            ],
        )  # type: ignore[misc]
        if user_info is not None:
            return UUID(bytes=user_info.get("user_id")), UUID(
                bytes=user_info.get("login_session_id")
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
        await self._redis_client.delete(
            self.generate_authentication_token_key(
                authentication_token_hash=authentication_token_hash,
            ),
        )
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
        authentication_token_keys = [
            self.generate_authentication_token_key(
                authentication_token_hash=str(authentication_token_hash),
            )
            for authentication_token_hash in authentication_token_hashes
        ]
        if authentication_token_keys:
            await self._redis_client.delete(*authentication_token_keys)
        await self._redis_client.delete(
            self.generate_token_owner_key(
                user_id=user_id,
            ),
        )

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
        # hash password reset token before storing
        reset_token_hash = self.hash_password_reset_token(
            password_reset_token=reset_token,
        )

        self._session.add(
            PasswordResetToken(
                user_id=user_id,
                token_hash=reset_token_hash,
                expires_at=expires_at,
            ),
        )
        await self._session.commit()
        return reset_token

    async def get_password_reset_token(
        self,
        reset_token_hash: str,
    ) -> PasswordResetToken | None:
        """Get a password reset token."""
        return await self._session.scalar(
            select(PasswordResetToken).where(
                PasswordResetToken.token_hash == reset_token_hash,
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
