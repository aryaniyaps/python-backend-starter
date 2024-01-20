from uuid import UUID

from argon2 import PasswordHasher
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User


class UserRepo:
    def __init__(
        self,
        session: AsyncSession,
        password_hasher: PasswordHasher,
    ) -> None:
        self._session = session
        self._password_hasher = password_hasher

    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        login_ip: str,
    ) -> User:
        """Create a new user."""
        user = User(
            username=username,
            email=email,
            # hash the password before storing
            password_hash=self.hash_password(
                password=password,
            ),
            last_login_ip=login_ip,
        )
        self._session.add(user)
        await self._session.commit()
        return user

    def hash_password(self, password: str) -> str:
        """Hash the given password."""
        return self._password_hasher.hash(
            password=password,
        )

    async def update_user(
        self,
        user: User,
        *,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        last_login_ip: str | None = None,
        update_last_login: bool = False,
    ) -> User:
        """Update the user with the given ID."""
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if password is not None:
            user.password_hash = self.hash_password(
                password=password,
            )
        if last_login_ip is not None:
            user.last_login_ip = last_login_ip
        if update_last_login:
            # we use `statement_timestamp()` here instead of `now()`
            # to set the current datetime even inside a transaction.
            user.last_login_at = text("statement_timestamp()")

        self._session.add(user)
        await self._session.commit()
        return user

    async def get_user_by_username(
        self,
        username: str,
    ) -> User | None:
        """Get a user by username."""
        return await self._session.scalar(
            select(User).where(
                User.username == username,
            ),
        )

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        """Get a user by ID."""
        return await self._session.scalar(
            select(User).where(
                User.id == user_id,
            ),
        )

    async def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """Get a user by email."""
        return await self._session.scalar(
            select(User).where(
                User.email == email,
            ),
        )
