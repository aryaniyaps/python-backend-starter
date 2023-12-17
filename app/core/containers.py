from enum import Enum

from argon2 import PasswordHasher
from di import Container, bind_by_type
from di.dependent import Dependent
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from app.auth.repos import AuthRepo
from app.auth.services import AuthService
from app.config import Settings
from app.core.database import get_database_connection, get_database_engine
from app.core.emails import EmailSender, get_email_sender
from app.core.redis_client import get_redis_client
from app.core.security import get_password_hasher
from app.users.repos import UserRepo
from app.users.services import UserService


class DIScope(Enum):
    """Enumeration representing dependency injection scopes."""

    APP = "app"
    REQUEST = "request"


def create_container() -> Container:
    """Initialze the dependency injection container."""
    container = Container()

    container.bind(
        bind_by_type(
            Dependent(
                lambda *_args: Settings(),  # type: ignore
                scope=DIScope.APP,
            ),
            Settings,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(
                get_database_engine,
                scope=DIScope.APP,
            ),
            AsyncEngine,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(
                get_database_connection,
                scope=DIScope.REQUEST,
            ),
            AsyncConnection,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(
                get_redis_client,
                scope=DIScope.APP,
            ),
            Redis,
        )
    )

    container.bind(
        bind_by_type(
            Dependent(
                get_email_sender,
                scope=DIScope.APP,
            ),
            EmailSender,
        )
    )

    container.bind(
        bind_by_type(
            Dependent(
                get_password_hasher,
                scope=DIScope.APP,
            ),
            PasswordHasher,
        )
    )

    container.bind(
        bind_by_type(
            Dependent(
                UserRepo,
                scope=DIScope.REQUEST,
            ),
            UserRepo,
        )
    )

    container.bind(
        bind_by_type(
            Dependent(
                AuthRepo,
                scope=DIScope.REQUEST,
            ),
            AuthRepo,
        )
    )

    container.bind(
        bind_by_type(
            Dependent(
                UserService,
                scope=DIScope.REQUEST,
            ),
            UserService,
        )
    )

    container.bind(
        bind_by_type(
            Dependent(
                AuthService,
                scope=DIScope.REQUEST,
            ),
            AuthService,
        )
    )

    return container
