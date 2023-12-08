from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterator

from aioinject import Container, providers
from redis.asyncio import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncConnection

from app.auth.repos import AuthRepo
from app.auth.services import AuthService
from app.config import settings
from app.core.database import engine
from app.core.emails import EmailSender
from app.users.repos import UserRepo
from app.users.services import UserService


@asynccontextmanager
async def get_database_connection() -> AsyncIterator[AsyncConnection]:
    """Get a database connection."""
    async with engine.connect() as connection:
        yield connection


def get_redis_client() -> Redis:
    """Get the redis client."""
    return from_url(
        url=str(settings.redis_url),
    )


def get_email_sender() -> Iterator[EmailSender]:
    """Get the email sender."""
    email_sender = EmailSender(
        email_server=settings.email_server,
        email_from=settings.email_from,
    )
    yield email_sender
    email_sender.close_connection()


def register_dependencies(container: Container) -> None:
    """Register dependencies for the container."""
    container.register(
        provider=providers.Callable(
            get_database_connection,
        )
    )
    container.register(
        provider=providers.Singleton(
            get_redis_client,
        )
    )
    container.register(
        provider=providers.Singleton(
            get_email_sender,
        )
    )
    container.register(
        provider=providers.Callable(
            AuthRepo,
        )
    )
    container.register(
        provider=providers.Callable(
            AuthService,
        )
    )
    container.register(
        provider=providers.Callable(
            UserRepo,
        )
    )
    container.register(
        provider=providers.Callable(
            UserService,
        )
    )


def create_container() -> Container:
    """Initialize a container."""
    container = Container()
    register_dependencies(container)
    return container


container = create_container()
