from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: UUID,
        email: str,
        display_name: str,
    ) -> User:
        """Create a new user."""
        user = User(
            id=user_id,
            display_name=display_name,
            email=email,
        )
        self._session.add(user)
        await self._session.commit()
        return user

    async def update(
        self,
        user: User,
        *,
        display_name: str | None = None,
        email: str | None = None,
    ) -> User:
        """Update the given user."""
        if display_name is not None:
            user.display_name = display_name

        if email is not None:
            user.email = email

        self._session.add(user)
        await self._session.commit()
        return user

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
