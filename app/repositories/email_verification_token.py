from hashlib import sha256
from secrets import token_urlsafe

from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.constants import EMAIL_VERIFICATION_TOKEN_EXPIRES_IN
from app.models.email_verification_token import EmailVerificationToken


class EmailVerificationTokenRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, email: str) -> str:
        """Create a new email verification token."""
        expires_at = text(
            f"NOW() + INTERVAL '{EMAIL_VERIFICATION_TOKEN_EXPIRES_IN} SECOND'",
        )

        verification_token = self.generate_token()

        email_verification_token = EmailVerificationToken(
            email=email,
            expires_at=expires_at,
            token_hash=self.hash_token(
                email_verification_token=verification_token,
            ),
        )
        self._session.add(email_verification_token)
        await self._session.commit()
        return verification_token

    async def get_by_token_email(
        self, verification_token: str, email: str
    ) -> EmailVerificationToken | None:
        """Get an email verification token by token and email."""
        return await self._session.scalar(
            select(EmailVerificationToken).where(
                EmailVerificationToken.token_hash
                == self.hash_token(
                    email_verification_token=verification_token,
                )
                and EmailVerificationToken.email == email,
            ),
        )

    async def delete_all(self, email: str) -> None:
        """Delete all email verification tokens for the given email."""
        await self._session.execute(
            delete(EmailVerificationToken).where(
                EmailVerificationToken.email == email,
            ),
        )

    @staticmethod
    def generate_token() -> str:
        """Generate an email verification token."""
        return token_urlsafe(16)

    @staticmethod
    def hash_token(email_verification_token: str) -> str:
        """Hash the given email verification token."""
        return sha256(email_verification_token.encode()).hexdigest()
