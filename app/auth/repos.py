from datetime import datetime
from hashlib import sha256
from secrets import token_hex
from typing import Awaitable
from uuid import UUID

from lagom import bind_to_container, injectable
from redis.asyncio import Redis
from sqlalchemy import insert, select, text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.auth.models import PasswordResetToken
from app.core.constants import PASSWORD_RESET_TOKEN_EXPIRES_IN
from app.core.containers import context_container

from .tables import password_reset_tokens_table


class AuthRepo:
    @classmethod
    @bind_to_container(container=context_container)
    async def create_authentication_token(
        cls,
        user_id: UUID,
        redis_client: Redis = injectable,
    ) -> str:
        """Create a new authentication token."""
        authentication_token = cls.generate_authentication_token()
        # hash authentication token before storing
        authentication_token_hash = cls.hash_authentication_token(
            authentication_token=authentication_token,
        )
        await redis_client.set(
            name=cls.generate_authentication_token_key(
                authentication_token_hash=authentication_token_hash,
            ),
            value=str(user_id),
        )
        await redis_client.sadd(
            cls.generate_token_owner_key(
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

    @classmethod
    @bind_to_container(container=context_container)
    async def get_user_id_from_authentication_token(
        cls,
        authentication_token: str,
        redis_client: Redis = injectable,
    ) -> UUID | None:
        """Get the user ID from the authentication token."""
        user_id = await redis_client.get(
            name=cls.generate_authentication_token_key(
                authentication_token_hash=cls.hash_authentication_token(
                    authentication_token=authentication_token,
                ),
            )
        )
        return UUID(user_id)

    @classmethod
    @bind_to_container(container=context_container)
    async def remove_authentication_token(
        cls,
        authentication_token: str,
        user_id: UUID,
        redis_client: Redis = injectable,
    ) -> None:
        """Remove the given authentication token."""
        authentication_token_hash = cls.hash_authentication_token(
            authentication_token=authentication_token,
        )
        await redis_client.delete(
            cls.generate_authentication_token_key(
                authentication_token_hash=authentication_token_hash,
            ),
        )
        await redis_client.srem(
            cls.generate_token_owner_key(
                user_id=user_id,
            ),
            authentication_token_hash,
        )  # type: ignore

    @classmethod
    @bind_to_container(container=context_container)
    async def remove_all_authentication_tokens(
        cls,
        user_id: UUID,
        redis_client: Redis = injectable,
    ) -> None:
        """Remove all authentication tokens for the given user ID."""
        authentication_token_hashes = await redis_client.get(
            name=cls.generate_token_owner_key(
                user_id=user_id,
            )
        )
        for authentication_token_hash in authentication_token_hashes:
            await redis_client.delete(
                cls.generate_authentication_token_key(
                    authentication_token_hash=authentication_token_hash,
                ),
            )
        await redis_client.delete(
            cls.generate_token_owner_key(
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

    @classmethod
    @bind_to_container(container=context_container)
    async def create_password_reset_token(
        cls,
        user_id: UUID,
        user_last_login_at: datetime,
        connection_maker: Awaitable[AsyncConnection] = injectable,
    ) -> str:
        """Create a new password reset token."""
        expires_at = text("NOW() + INTERVAL ':expires_in SECOND'").bindparams(
            expires_in=PASSWORD_RESET_TOKEN_EXPIRES_IN
        )

        reset_token = cls.generate_password_reset_token()
        # hash password reset token before storing
        reset_token_hash = cls.hash_password_reset_token(
            password_reset_token=reset_token,
        )

        connection = await connection_maker
        await connection.execute(
            insert(password_reset_tokens_table)
            .values(
                user_id=user_id,
                token_hash=reset_token_hash,
                expires_at=expires_at,
                last_login_at=user_last_login_at,
            )
            .returning(*password_reset_tokens_table.c),
        )
        return reset_token

    @classmethod
    @bind_to_container(container=context_container)
    async def get_password_reset_token(
        cls,
        reset_token_hash: str,
        connection_maker: Awaitable[AsyncConnection] = injectable,
    ) -> PasswordResetToken | None:
        """Get a password reset token."""
        connection = await connection_maker
        result = await connection.execute(
            select(*password_reset_tokens_table.c).where(
                password_reset_tokens_table.c.token_hash == reset_token_hash
            )
        )
        reset_token_row = result.one_or_none()
        if reset_token_row:
            return PasswordResetToken(**reset_token_row._mapping)
