from datetime import datetime
from hashlib import sha256
from secrets import token_hex
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy import insert, select, text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.auth.models import PasswordResetToken
from app.core.constants import PASSWORD_RESET_TOKEN_EXPIRES_IN
from app.core.database import get_database_connection
from app.core.redis_client import get_redis_client

from .tables import password_reset_tokens_table


class AuthRepo:
    def __init__(
        self,
        connection: Annotated[
            AsyncConnection,
            Depends(
                dependency=get_database_connection,
            ),
        ],
        redis_client: Annotated[
            Redis,
            Depends(
                dependency=get_redis_client,
            ),
        ],
    ) -> None:
        self._connection = connection
        self._redis_client = redis_client

    async def create_authentication_token(
        self,
        user_id: UUID,
    ) -> str:
        """Create a new authentication token."""
        authentication_token = self.generate_authentication_token()
        # hash authentication token before storing
        authentication_token_hash = self.hash_authentication_token(
            authentication_token=authentication_token,
        )
        await self._redis_client.set(
            name=self.generate_authentication_token_key(
                authentication_token_hash=authentication_token_hash,
            ),
            value=user_id.bytes,
        )
        await self._redis_client.sadd(
            self.generate_token_owner_key(
                user_id=user_id,
            ),
            authentication_token_hash,
        )  # type: ignore
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

    async def get_user_id_from_authentication_token(
        self,
        authentication_token: str,
    ) -> UUID | None:
        """Get the user ID from the authentication token."""
        user_id = await self._redis_client.get(
            name=self.generate_authentication_token_key(
                authentication_token_hash=self.hash_authentication_token(
                    authentication_token=authentication_token,
                ),
            )
        )
        if user_id is not None:
            return UUID(bytes=user_id)

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
        )  # type: ignore

    async def remove_all_authentication_tokens(
        self,
        user_id: UUID,
    ) -> None:
        """Remove all authentication tokens for the given user ID."""
        authentication_token_hashes = await self._redis_client.smembers(
            name=self.generate_token_owner_key(
                user_id=user_id,
            )
        )  # type: ignore
        authentication_token_keys = [
            self.generate_authentication_token_key(
                authentication_token_hash=authentication_token_hash
            )
            for authentication_token_hash in authentication_token_hashes
        ]
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
        last_login_at: datetime,
    ) -> str:
        """Create a new password reset token."""
        expires_at = text(
            f"NOW() + INTERVAL '{PASSWORD_RESET_TOKEN_EXPIRES_IN} SECOND'"
        )

        reset_token = self.generate_password_reset_token()
        # hash password reset token before storing
        reset_token_hash = self.hash_password_reset_token(
            password_reset_token=reset_token,
        )

        await self._connection.execute(
            insert(password_reset_tokens_table)
            .values(
                user_id=user_id,
                token_hash=reset_token_hash,
                expires_at=expires_at,
                last_login_at=last_login_at,
            )
            .returning(*password_reset_tokens_table.c),
        )
        return reset_token

    async def get_password_reset_token(
        self,
        reset_token_hash: str,
    ) -> PasswordResetToken | None:
        """Get a password reset token."""
        result = await self._connection.execute(
            select(*password_reset_tokens_table.c).where(
                password_reset_tokens_table.c.token_hash == reset_token_hash
            )
        )
        reset_token_row = result.one_or_none()
        if reset_token_row:
            return PasswordResetToken.model_validate(reset_token_row)
