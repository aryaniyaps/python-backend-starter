from uuid import UUID

from sqlalchemy import delete, insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app.containers import container
from app.core.security import password_hasher
from app.users.models import User

from .tables import users_table


class UserRepo:
    @classmethod
    async def create_user(
        cls,
        username: str,
        email: str,
        password: str,
    ) -> User:
        """Create a new user."""
        async with container.resolve(AsyncConnection) as connection:
            result = await connection.execute(
                insert(users_table)
                .values(
                    username=username,
                    email=email,
                    # hash the password before storing
                    password_hash=cls.hash_password(
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

    @classmethod
    async def delete_user(
        cls,
        user_id: UUID,
    ) -> None:
        """Delete a user with the given ID."""
        async with container.resolve(AsyncConnection) as connection:
            await connection.execute(
                delete(users_table).where(
                    users_table.c.id == user_id,
                ),
            )

    @classmethod
    async def update_user_password(
        cls,
        user_id: UUID,
        password_hash: str | None = None,
    ) -> User | None:
        """Update the password for the user with the given ID."""
        user = await cls.get_user_by_id(user_id=user_id)
        if not user:
            return

        async with container.resolve(AsyncConnection) as connection:
            result = await connection.execute(
                update(users_table)
                .where(users_table.c.id == user_id)
                .values(password_hash=password_hash)
                .returning(*users_table.c),
            )
        updated_user_row = result.one()
        return User(**updated_user_row._mapping)

    @classmethod
    async def update_user_last_login(
        cls,
        user_id: UUID,
    ) -> User | None:
        """Update the last login timestamp to now for the user with the given ID."""
        user = await cls.get_user_by_id(user_id=user_id)
        if not user:
            return

        async with container.resolve(AsyncConnection) as connection:
            result = await connection.execute(
                update(users_table)
                .where(users_table.c.id == user_id)
                .values(last_login_at=text("NOW()"))
                .returning(*users_table.c),
            )
        updated_user_row = result.one()
        return User(**updated_user_row._mapping)

    @classmethod
    async def get_user_by_username(
        cls,
        username: str,
    ) -> User | None:
        """Get a user by Username."""
        async with container.resolve(AsyncConnection) as connection:
            result = await connection.execute(
                select(*users_table.c).where(users_table.c.username == username)
            )
        user_row = result.one_or_none()
        if user_row:
            return User(**user_row._mapping)

    @classmethod
    async def get_user_by_id(
        cls,
        user_id: UUID,
    ) -> User | None:
        """Get a user by ID."""
        async with container.resolve(AsyncConnection) as connection:
            result = await connection.execute(
                select(*users_table.c).where(users_table.c.id == user_id)
            )
        user_row = result.one_or_none()
        if user_row:
            return User(**user_row._mapping)

    @classmethod
    async def get_user_by_email(
        cls,
        email: str,
    ) -> User | None:
        """Get a user by email."""
        async with container.resolve(AsyncConnection) as connection:
            result = await connection.execute(
                select(*users_table.c).where(users_table.c.email == email)
            )
        user_row = result.one_or_none()
        if user_row:
            return User(**user_row._mapping)
