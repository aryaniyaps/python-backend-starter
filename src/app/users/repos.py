from sqlalchemy import insert, select, update
from app.core.database import engine
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
        async with engine.connect() as connection:
            result = await connection.execute(
                insert(users_table)
                .values(
                    username=username,
                    email=email,
                    password=password,
                )
                .returning(
                    users_table.c.id,
                    users_table.c.username,
                    users_table.c.email,
                    users_table.c.password,
                    users_table.c.created_at,
                    users_table.c.updated_at,
                ),
            )
            user_row = result.scalar_one()
            return User(**user_row)

    @classmethod
    async def update_user(
        cls,
        user_id: int,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> User | None:
        """Update the user with the given ID."""
        user = await cls.get_user_by_id(user_id=user_id)
        if not user:
            return

        update_data = {}

        if username is not None:
            update_data["username"] = username
        if email is not None:
            update_data["email"] = email
        if password is not None:
            update_data["password"] = password

        async with engine.connect() as connection:
            result = await connection.execute(
                update(users_table)
                .where(users_table.c.id == user_id)
                .values(**update_data)
                .returning(
                    users_table.c.id,
                    users_table.c.username,
                    users_table.c.email,
                    users_table.c.password,
                    users_table.c.created_at,
                    users_table.c.updated_at,
                ),
            )
            updated_user_row = result.scalar_one()
            return User(**updated_user_row)

    @classmethod
    async def get_user_by_username(cls, username: str) -> User | None:
        """Get a user by Username."""
        async with engine.connect() as connection:
            result = await connection.execute(
                select(
                    users_table.c.id,
                    users_table.c.username,
                    users_table.c.email,
                    users_table.c.password,
                    users_table.c.created_at,
                    users_table.c.updated_at,
                ).where(users_table.c.username == username)
            )
            user_row = result.scalar_one_or_none()
            if user_row:
                return User(**user_row)

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> User | None:
        """Get a user by ID."""
        async with engine.connect() as connection:
            result = await connection.execute(
                select(
                    users_table.c.id,
                    users_table.c.username,
                    users_table.c.email,
                    users_table.c.password,
                    users_table.c.created_at,
                    users_table.c.updated_at,
                ).where(users_table.c.id == user_id)
            )
            user_row = result.scalar_one_or_none()
            if user_row:
                return User(**user_row)

    @classmethod
    async def get_user_by_email(cls, email: str) -> User | None:
        """Get a user by email."""
        async with engine.connect() as connection:
            result = await connection.execute(
                select(
                    users_table.c.id,
                    users_table.c.username,
                    users_table.c.email,
                    users_table.c.password,
                    users_table.c.created_at,
                    users_table.c.updated_at,
                ).where(users_table.c.email == email)
            )
            user_row = result.scalar_one_or_none()
            if user_row:
                return User(**user_row)
