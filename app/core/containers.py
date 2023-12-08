from typing import AsyncIterator, Iterator

from lagom import Container, context_dependency_definition, dependency_definition
from lagom.experimental.context_based import AsyncContextContainer
from redis.asyncio import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncConnection

from app.config import settings
from app.core.database import engine
from app.core.emails import EmailSender

container = Container()


@context_dependency_definition(container=container)
async def get_database_connection() -> AsyncIterator[AsyncConnection]:
    """Get a database connection"""
    async with engine.begin() as connection:
        yield connection


@context_dependency_definition(container=container)
def get_email_sender() -> Iterator[EmailSender]:
    """Get the email sender."""
    email_sender = EmailSender(
        email_server=settings.email_server,
        email_from=settings.email_from,
    )
    yield email_sender
    email_sender.close_connection()


@dependency_definition(container=container, singleton=True)
def get_redis_client() -> Redis:
    """Get the redis client."""
    return from_url(
        url=str(settings.redis_url),
    )


context_container = AsyncContextContainer(
    container=container,
    context_types=[
        AsyncConnection,
    ],
    context_singletons=[
        EmailSender,
    ],
)
