import secrets
import string
from hashlib import sha256

from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import now

from app.lib.constants import EMAIL_VERIFICATION_CODE_EXPIRES_IN
from app.models.email_verification_code import EmailVerificationCode


class EmailVerificationCodeRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def generate_code() -> str:
        """Generate an email verification code."""
        return "".join(secrets.choice(string.digits) for i in range(8))

    @staticmethod
    def hash_code(email_verification_code: str) -> str:
        """Hash the given email verification code."""
        return sha256(email_verification_code.encode()).hexdigest()

    async def create(self, email: str) -> str:
        """Create a new email verification code."""
        expires_at = text(
            f"NOW() + INTERVAL '{EMAIL_VERIFICATION_CODE_EXPIRES_IN} SECOND'",
        )

        verification_code = self.generate_code()

        email_verification_code = EmailVerificationCode(
            email=email,
            expires_at=expires_at,
            # hash code before storing
            code_hash=self.hash_code(
                email_verification_code=verification_code,
            ),
        )
        self._session.add(email_verification_code)
        await self._session.commit()
        return verification_code

    async def get_by_code_email(
        self, verification_code: str, email: str
    ) -> EmailVerificationCode | None:
        """Get an email verification code by code and email."""
        return await self._session.scalar(
            select(EmailVerificationCode).where(
                EmailVerificationCode.code_hash
                == self.hash_code(
                    email_verification_code=verification_code,
                )
                and EmailVerificationCode.email == email,
            ),
        )

    async def delete_all(self, email: str) -> None:
        """Delete all email verification codes for the given email."""
        await self._session.execute(
            delete(EmailVerificationCode).where(
                EmailVerificationCode.email == email,
            ),
        )

    async def delete_expired(self) -> None:
        """Delete all email verification codes which have expired."""
        await self._session.execute(
            delete(EmailVerificationCode).where(
                EmailVerificationCode.expires_at <= now(),
            ),
        )
