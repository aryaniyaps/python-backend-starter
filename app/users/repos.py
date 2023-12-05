from typing import Awaitable

from lagom import bind_to_container, injectable
from sqlalchemy import delete, insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app.core.containers import context_container
from app.users.models import User

from .tables import users_table


class UserRepo:
    @classmethod
    @bind_to_container(container=context_container)
    async def create_user(
        cls,
        username: str,
        email: str,
        password_hash: str,
        connection_maker: Awaitable[AsyncConnection] = injectable,
    ) -> User:
        """Create a new user."""
        connection = await connection_maker
        result = await connection.execute(
            insert(users_table)
            .values(
                username=username,
                email=email,
                password_hash=password_hash,
            )
            .returning(*users_table.c),
        )
        user_row = result.one()
        return User(**user_row._mapping)

    @classmethod
    @bind_to_container(container=context_container)
    async def delete_user(
        cls,
        user_id: int,
        connection_maker: Awaitable[AsyncConnection] = injectable,
    ) -> None:
        """Delete a user with the given ID."""
        connection = await connection_maker
        await connection.execute(
            delete(users_table).where(
                users_table.c.id == user_id,
            ),
        )

    @classmethod
    @bind_to_container(container=context_container)
    async def update_user_password(
        cls,
        user_id: int,
        password_hash: str | None = None,
        connection_maker: Awaitable[AsyncConnection] = injectable,
    ) -> User | None:
        """Update the password for the user with the given ID."""
        user = await cls.get_user_by_id(user_id=user_id)
        if not user:
            return

        connection = await connection_maker
        result = await connection.execute(
            update(users_table)
            .where(users_table.c.id == user_id)
            .values(password_hash=password_hash)
            .returning(*users_table.c),
        )
        updated_user_row = result.one()
        return User(**updated_user_row._mapping)

    @classmethod
    @bind_to_container(container=context_container)
    async def update_user_last_login(
        cls,
        user_id: int,
        connection_maker: Awaitable[AsyncConnection] = injectable,
    ) -> User | None:
        """Update the last login timestamp to now for the user with the given ID."""
        user = await cls.get_user_by_id(user_id=user_id)
        if not user:
            return

        connection = await connection_maker
        result = await connection.execute(
            update(users_table)
            .where(users_table.c.id == user_id)
            .values(last_login_at=text("NOW()"))
            .returning(*users_table.c),
        )
        updated_user_row = result.one()
        return User(**updated_user_row._mapping)

    @classmethod
    @bind_to_container(container=context_container)
    async def get_user_by_username(
        cls,
        username: str,
        connection_maker: Awaitable[AsyncConnection] = injectable,
    ) -> User | None:
        """Get a user by Username."""
        connection = await connection_maker
        result = await connection.execute(
            select(*users_table.c).where(users_table.c.username == username)
        )
        user_row = result.one_or_none()
        if user_row:
            return User(**user_row._mapping)

    @classmethod
    @bind_to_container(container=context_container)
    async def get_user_by_id(
        cls,
        user_id: int,
        connection_maker: Awaitable[AsyncConnection] = injectable,
    ) -> User | None:
        """Get a user by ID."""
        connection = await connection_maker
        result = await connection.execute(
            select(*users_table.c).where(users_table.c.id == user_id)
        )
        user_row = result.one_or_none()
        if user_row:
            return User(**user_row._mapping)

    @classmethod
    @bind_to_container(container=context_container)
    async def get_user_by_email(
        cls,
        email: str,
        connection_maker: Awaitable[AsyncConnection] = injectable,
    ) -> User | None:
        """Get a user by email."""
        connection = await connection_maker
        result = await connection.execute(
            select(*users_table.c).where(users_table.c.email == email)
        )
        user_row = result.one_or_none()
        if user_row:
            return User(**user_row._mapping)
