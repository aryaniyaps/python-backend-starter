import secrets
import string
from hashlib import sha256
from uuid import UUID

import backoff
from sqlalchemy import delete, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import now

from app.lib.constants import PASSWORD_RESET_CODE_EXPIRES_IN
from app.models.password_reset_code import PasswordResetCode


class PasswordResetCodeRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def generate_code() -> str:
        """Generate a password reset code."""
        return "".join(secrets.choice(string.digits) for i in range(8))

    @staticmethod
    def hash_code(password_reset_code: str) -> str:
        """Hash the given password reset code."""
        return sha256(password_reset_code.encode()).hexdigest()

    @backoff.on_exception(
        backoff.constant,
        exception=IntegrityError,
        max_tries=2,
    )
    async def create(
        self,
        user_id: UUID,
    ) -> str:
        """Create a new password reset code."""
        expires_at = text(
            f"NOW() + INTERVAL '{PASSWORD_RESET_CODE_EXPIRES_IN} SECOND'",
        )

        reset_code = self.generate_code()

        self._session.add(
            PasswordResetCode(
                user_id=user_id,
                # hash password reset code before storing
                code_hash=self.hash_code(
                    password_reset_code=reset_code,
                ),
                expires_at=expires_at,
            ),
        )
        await self._session.commit()
        return reset_code

    async def get_by_reset_code(
        self,
        reset_code: str,
    ) -> PasswordResetCode | None:
        """Get a password reset code by reset code."""
        return await self._session.scalar(
            select(PasswordResetCode).where(
                PasswordResetCode.code_hash == self.hash_code(reset_code),
            ),
        )

    async def delete_all(
        self,
        user_id: UUID,
    ) -> None:
        """Delete password reset codes for the given user ID."""
        await self._session.execute(
            delete(PasswordResetCode).where(
                PasswordResetCode.user_id == user_id,
            ),
        )

    async def delete_expired(self) -> None:
        """Delete all password reset codes which have expired."""
        await self._session.execute(
            delete(PasswordResetCode).where(
                PasswordResetCode.expires_at <= now(),
            ),
        )
