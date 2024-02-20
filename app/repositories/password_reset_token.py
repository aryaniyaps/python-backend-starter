from hashlib import sha256
from secrets import token_urlsafe
from uuid import UUID

from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.constants import PASSWORD_RESET_TOKEN_EXPIRES_IN
from app.models.password_reset_token import PasswordResetToken


class PasswordResetTokenRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def generate_token() -> str:
        """Generate a password reset token."""
        return token_urlsafe(16)

    @staticmethod
    def hash_token(password_reset_token: str) -> str:
        """Hash the given password reset token."""
        return sha256(password_reset_token.encode()).hexdigest()

    async def create(
        self,
        user_id: UUID,
    ) -> str:
        """Create a new password reset token."""
        expires_at = text(
            f"NOW() + INTERVAL '{PASSWORD_RESET_TOKEN_EXPIRES_IN} SECOND'",
        )

        reset_token = self.generate_token()

        self._session.add(
            PasswordResetToken(
                user_id=user_id,
                # hash password reset token before storing
                token_hash=self.hash_token(
                    password_reset_token=reset_token,
                ),
                expires_at=expires_at,
            ),
        )
        await self._session.commit()
        return reset_token

    async def get_by_reset_token(
        self,
        reset_token: str,
    ) -> PasswordResetToken | None:
        """Get a password reset token by reset token."""
        return await self._session.scalar(
            select(PasswordResetToken).where(
                PasswordResetToken.token_hash == self.hash_token(reset_token),
            ),
        )

    async def delete_all(
        self,
        user_id: UUID,
    ) -> None:
        """Delete password reset tokens for the given user ID."""
        await self._session.execute(
            delete(PasswordResetToken).where(
                PasswordResetToken.user_id == user_id,
            ),
        )
