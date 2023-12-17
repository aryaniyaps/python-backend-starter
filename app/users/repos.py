from uuid import UUID

from argon2 import PasswordHasher
from sqlalchemy import insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app.users.models import User

from .tables import users_table


class UserRepo:
    def __init__(
        self,
        connection: AsyncConnection,
        password_hasher: PasswordHasher,
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
        user_row = result.one()
        return User.model_validate(user_row)

    def hash_password(self, password: str) -> str:
        """Hash the given password."""
        return self._password_hasher.hash(
            password=password,
        )

    async def update_user_password(
        self,
        user_id: UUID,
        password: str,
    ) -> User | None:
        """Update the password for the user with the given ID."""
        user = await self.get_user_by_id(user_id=user_id)
        if not user:
            return

        result = await self._connection.execute(
            update(users_table)
            .where(users_table.c.id == user_id)
            .values(
                password_hash=self.hash_password(
                    password=password,
                )
            )
            .returning(*users_table.c),
        )
        updated_user_row = result.one()
        return User.model_validate(updated_user_row)

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
        return User.model_validate(updated_user_row)

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
        print("GETTING USER BY EMAIL")
        result = await self._connection.execute(
            select(*users_table.c).where(users_table.c.email == email)
        )
        user_row = result.one_or_none()
        if user_row:
            return User.model_validate(user_row)
