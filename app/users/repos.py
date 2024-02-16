from hashlib import sha256
from secrets import token_hex
from uuid import UUID

from argon2 import PasswordHasher
from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import EMAIL_VERIFICATION_TOKEN_EXPIRES_IN
from app.users.models import EmailVerificationToken, User


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
        return token_hex(32)

    @staticmethod
    def hash_token(email_verification_token: str) -> str:
        """Hash the given email verification token."""
        return sha256(email_verification_token.encode()).hexdigest()


class UserRepo:
    def __init__(
        self,
        session: AsyncSession,
        password_hasher: PasswordHasher,
    ) -> None:
        self._session = session
        self._password_hasher = password_hasher

    async def create(
        self,
        username: str,
        email: str,
        password: str,
    ) -> User:
        """Create a new user."""
        user = User(
            username=username,
            email=email,
            # hash the password before storing
            password_hash=self.hash_password(
                password=password,
            ),
        )
        self._session.add(user)
        await self._session.commit()
        return user

    async def update(
        self,
        user: User,
        *,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> User:
        """Update the given user."""
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if password is not None:
            user.password_hash = self.hash_password(
                password=password,
            )

        self._session.add(user)
        await self._session.commit()
        return user

    def hash_password(self, password: str) -> str:
        """Hash the given password."""
        return self._password_hasher.hash(
            password=password,
        )

    async def get(
        self,
        user_id: UUID,
    ) -> User | None:
        """Get an user by ID."""
        return await self._session.scalar(
            select(User).where(
                User.id == user_id,
            ),
        )

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:
        """Get an user by username."""
        return await self._session.scalar(
            select(User).where(
                User.username == username,
            ),
        )

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """Get an user by email."""
        return await self._session.scalar(
            select(User).where(
                User.email == email,
            ),
        )
