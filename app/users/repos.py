from uuid import UUID

from sqlalchemy import insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app.core.security import password_hasher
from app.users.models import User

from .tables import users_table


class UserRepo:
    def __init__(
        self,
        connection: AsyncConnection,
    ) -> None:
        self._connection = connection

    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> User:
        """Create a new user."""
        result = await self._connection.execute(
            insert(users_table)
            .values(
                username=username,
                email=email,
                # hash the password before storing
                password_hash=self.hash_password(
                    password=password,
                ),
            )
            .returning(*users_table.c),
        )
        user_row = result.one()
        return User(**user_row._mapping)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the given password."""
        return password_hasher.hash(
            password=password,
        )

    async def update_user_password(
        self,
        user_id: UUID,
        password_hash: str | None = None,
    ) -> User | None:
        """Update the password for the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)
        if not user:
            return

        result = await self._connection.execute(
            update(users_table)
            .where(users_table.c.id == user_id)
            .values(password_hash=password_hash)
            .returning(*users_table.c),
        )
        updated_user_row = result.one()
        return User(**updated_user_row._mapping)

    async def update_user_last_login(
        self,
        user_id: UUID,
    ) -> User | None:
        """Update the last login timestamp to now for the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)
        if not user:
            return

        result = await self._connection.execute(
            update(users_table)
            .where(users_table.c.id == user_id)
            .values(last_login_at=text("NOW()"))
            .returning(*users_table.c),
        )
        updated_user_row = result.one()
        return User(**updated_user_row._mapping)

    async def get_user_by_username(
        self,
        username: str,
    ) -> User | None:
        """Get a user by Username."""
        result = await self._connection.execute(
            select(*users_table.c).where(users_table.c.username == username)
        )
        user_row = result.one_or_none()
        if user_row:
            return User(**user_row._mapping)

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        """Get a user by ID."""
        result = await self._connection.execute(
            select(*users_table.c).where(users_table.c.id == user_id)
        )
        user_row = result.one_or_none()
        if user_row:
            return User(**user_row._mapping)

    async def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """Get a user by email."""
        result = await self._connection.execute(
            select(*users_table.c).where(users_table.c.email == email)
        )
        user_row = result.one_or_none()
        if user_row:
            return User(**user_row._mapping)
