from typing import Annotated
from uuid import UUID

from argon2 import PasswordHasher
from fastapi import Depends
from sqlalchemy import insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app.core.database import get_database_connection
from app.core.security import get_password_hasher
from app.users.models import User

from .tables import users_table


class UserRepo:
    def __init__(
        self,
        connection: Annotated[
            AsyncConnection,
            Depends(
                dependency=get_database_connection,
            ),
        ],
        password_hasher: Annotated[
            PasswordHasher,
            Depends(
                dependency=get_password_hasher,
            ),
        ],
    ) -> None:
        self._connection = connection
        self._password_hasher = password_hasher

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
        return User.model_validate(result.one())

    def hash_password(self, password: str) -> str:
        """Hash the given password."""
        return self._password_hasher.hash(
            password=password,
        )

    async def update_user(
        self,
        user_id: UUID,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        update_last_login: bool = False,
    ) -> User:
        """Update the user with the given ID."""
        values = {}
        if update_last_login:
            values["last_login_at"] = text("NOW()")
        if username is not None:
            values["username"] = username
        if email is not None:
            values["email"] = email
        if password is not None:
            values["password_hash"] = self.hash_password(
                password=password,
            )

        result = await self._connection.execute(
            update(users_table)
            .where(users_table.c.id == user_id)
            .values(**values)
            .returning(*users_table.c),
        )
        return User.model_validate(result.one())

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
            return User.model_validate(user_row)

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
            return User.model_validate(user_row)

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
            return User.model_validate(user_row)
