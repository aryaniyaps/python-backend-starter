from datetime import datetime
from hashlib import sha256
from secrets import token_hex

from sqlalchemy import insert, select, text

from app.auth.models import PasswordResetToken
from app.core.constants import PASSWORD_RESET_TOKEN_EXPIRES_IN
from app.core.database import engine
from app.core.redis_client import redis_client

from .tables import password_reset_tokens_table


class AuthRepo:
    @classmethod
    async def create_authentication_token(
        cls,
        user_id: int,
    ) -> str:
        """Create a new authentication token."""
        authentication_token = cls.generate_authentication_token()
        await redis_client.set(
            name=cls.generate_authentication_token_key(
                authentication_token=authentication_token,
            ),
            value=user_id,
        )
        return authentication_token

    @staticmethod
    def generate_authentication_token() -> str:
        """Generate an authentication token."""
        # Generate a random token
        return token_hex(32)

    @staticmethod
    def generate_authentication_token_key(authentication_token: str) -> str:
        """Generate a key for the authentication token."""
        return f"auth-token:${authentication_token}"

    @classmethod
    async def verify_authentication_token(
        cls,
        authentication_token: str,
    ) -> int | None:
        """
        Verify the given authentication token and
        return the corresponding user ID, if the token is valid.
        """
        user_id = await redis_client.get(
            name=cls.generate_authentication_token_key(
                authentication_token=authentication_token,
            )
        )
        return user_id

    @classmethod
    async def remove_authentication_token(cls, authentication_token: str) -> None:
        """Remove the given authentication token."""
        await redis_client.delete(
            cls.generate_authentication_token_key(
                authentication_token=authentication_token,
            ),
        )

    @staticmethod
    def generate_password_reset_token() -> str:
        """Generate a password reset token."""
        # Generate a random token
        return token_hex(32)

    @classmethod
    async def create_password_reset_token(
        cls, user_id: int, user_last_login_at: datetime
    ) -> str:
        """Create a new password reset token."""
        expires_at = text("(NOW() + INTERVAL :expires_in SECOND)").params(
            expires_in=PASSWORD_RESET_TOKEN_EXPIRES_IN
        )

        reset_token = cls.generate_password_reset_token()
        # hash password reset token before storing
        reset_token_hash = sha256(reset_token.encode()).hexdigest()

        async with engine.connect() as connection:
            await connection.execute(
                insert(password_reset_tokens_table)
                .values(
                    user_id=user_id,
                    token_hash=reset_token_hash,
                    expires_at=expires_at,
                    last_login_at=user_last_login_at,
                )
                .returning(
                    password_reset_tokens_table.c.id,
                    password_reset_tokens_table.c.user_id,
                    password_reset_tokens_table.c.token_hash,
                    password_reset_tokens_table.c.last_login_at,
                    password_reset_tokens_table.c.created_at,
                    password_reset_tokens_table.c.expires_at,
                ),
            )
            return reset_token

    @classmethod
    async def get_password_reset_token(
        cls,
        reset_token_hash: str,
    ) -> PasswordResetToken | None:
        """
        Get a password reset token.
        """
        async with engine.connect() as connection:
            result = await connection.execute(
                select(
                    password_reset_tokens_table.c.id,
                    password_reset_tokens_table.c.user_id,
                    password_reset_tokens_table.c.token_hash,
                    password_reset_tokens_table.c.last_login_at,
                    password_reset_tokens_table.c.created_at,
                    password_reset_tokens_table.c.expires_at,
                ).where(password_reset_tokens_table.c.token_hash == reset_token_hash)
            )
            reset_token_row = result.scalar_one_or_none()
            if reset_token_row:
                return PasswordResetToken(**reset_token_row)
