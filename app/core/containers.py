from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator, Iterator

import inject
from argon2 import PasswordHasher
from redis.asyncio import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncConnection

from app.config import settings
from app.core.database import engine
from app.core.emails import EmailSender


@asynccontextmanager
async def get_database_connection() -> AsyncIterator[AsyncConnection]:
    """Get a database connection."""
    async with engine.begin() as connection:
        yield connection


@asynccontextmanager
async def get_redis_client() -> AsyncIterator[Redis]:
    """Get the redis client."""
    redis_client = from_url(
        url=str(settings.redis_url),
    )
    yield redis_client

    await redis_client.aclose()


@contextmanager
def get_email_sender() -> Iterator[EmailSender]:
    """Get the email sender."""
    email_sender = EmailSender(
        email_server=settings.email_server,
        email_from=settings.email_from,
    )
    yield email_sender
    email_sender.close_connection()


def app_config(binder: inject.Binder) -> None:
    """Configure dependencies for the binder."""
    binder.bind_to_constructor(
        EmailSender,
        get_email_sender,
    )
    binder.bind_to_constructor(
        Redis,
        get_redis_client,
    )
    binder.bind_to_provider(
        AsyncConnection,
        get_database_connection,
    )
    binder.bind(
        PasswordHasher,
        PasswordHasher(),
    )


inject.configure(app_config)
