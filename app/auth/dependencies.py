from typing import Annotated
from uuid import UUID

from argon2 import PasswordHasher
from fastapi import Depends, Header
from geoip2.database import Reader
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repos import AuthRepo
from app.auth.services import AuthService
from app.core.database import get_database_session
from app.core.errors import UnauthenticatedError
from app.core.geo_ip import get_geoip_reader
from app.core.redis_client import get_redis_client
from app.core.security import get_password_hasher
from app.users.dependencies import get_user_repo
from app.users.repos import UserRepo


def get_auth_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
    redis_client: Annotated[
        Redis,
        Depends(
            dependency=get_redis_client,
        ),
    ],
) -> AuthRepo:
    """Get the auth repo."""
    return AuthRepo(
        session=session,
        redis_client=redis_client,
    )


def get_auth_service(
    auth_repo: Annotated[
        AuthRepo,
        Depends(
            dependency=get_auth_repo,
        ),
    ],
    user_repo: Annotated[
        UserRepo,
        Depends(
            dependency=get_user_repo,
        ),
    ],
    password_hasher: Annotated[
        PasswordHasher,
        Depends(
            dependency=get_password_hasher,
        ),
    ],
    geoip_reader: Annotated[
        Reader,
        Depends(
            dependency=get_geoip_reader,
        ),
    ],
) -> AuthService:
    """Get the auth service."""
    return AuthService(
        auth_repo=auth_repo,
        user_repo=user_repo,
        password_hasher=password_hasher,
        geoip_reader=geoip_reader,
    )


async def get_authentication_token(
    x_authentication_token: Annotated[str | None, Header()] = None,
) -> str:
    """Get the authentication token."""
    if not x_authentication_token:
        raise UnauthenticatedError(
            message="Authentication token is missing.",
        )
    return x_authentication_token


async def get_current_user_id(
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
    authentication_token: Annotated[
        str,
        Depends(
            dependency=get_authentication_token,
        ),
    ],
) -> UUID:
    """Get the current user ID."""
    # Verify the token and get the current user ID
    (
        user_id,
        login_session_id,
    ) = await auth_service.get_user_info_for_authentication_token(
        authentication_token=authentication_token,
    )
    return user_id
