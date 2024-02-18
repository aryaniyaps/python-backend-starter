from uuid import UUID

from argon2 import PasswordHasher
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_password import UserPassword


class UserPasswordRepo:
    def __init__(
        self,
        session: AsyncSession,
        password_hasher: PasswordHasher,
    ) -> None:
        self._session = session
        self._password_hasher = password_hasher

    async def create(
        self,
        user_id: UUID,
        password: str,
    ) -> UserPassword:
        """Create a new user password."""
        created_password = UserPassword(
            user_id=user_id,
            hash=self.hash_password(
                password=password,
            ),
        )
        self._session.add(created_password)
        await self._session.commit()
        return created_password

    def hash_password(self, password: str) -> str:
        """Hash the given password."""
        return self._password_hasher.hash(
            password=password,
        )

    async def get(self, user_id: UUID) -> UserPassword | None:
        """Get the user password for the given user ID."""
        return await self._session.scalar(
            select(UserPassword).where(
                UserPassword.user_id == user_id,
            ),
        )

    async def update(
        self,
        user_password: UserPassword,
        password: str,
    ) -> None:
        """Update the user password with the given ID."""
        user_password.hash = self.hash_password(
            password=password,
        )
        self._session.add(user_password)
        await self._session.commit()
