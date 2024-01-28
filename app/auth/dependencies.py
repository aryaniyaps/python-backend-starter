from typing import Annotated
from uuid import UUID

from argon2 import PasswordHasher
from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
from geoip2.database import Reader
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repos import AuthRepo
from app.auth.services import AuthService
from app.core.database import get_database_session
from app.core.geo_ip import get_geoip_reader
from app.core.redis_client import get_redis_client
from app.core.security import get_password_hasher
from app.users.dependencies import get_user_repo
from app.users.repos import UserRepo

authentication_token_header = APIKeyHeader(name="X-Authentication-Token")


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
    geoip_reader: Annotated[
        Reader,
        Depends(
            dependency=get_geoip_reader,
        ),
    ],
) -> AuthRepo:
    """Get the auth repo."""
    return AuthRepo(
        session=session,
        redis_client=redis_client,
        geoip_reader=geoip_reader,
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


async def get_current_user_id(
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=get_auth_service,
        ),
    ],
    authentication_token: Annotated[
        str,
        Security(
            authentication_token_header,
        ),
    ],
) -> UUID:
    """Get the current user ID."""
    # Verify the token and get the current user ID
    (
        user_id,
        login_session_id,
    ) = await auth_service.verify_authentication_token(
        authentication_token=authentication_token,
    )
    return user_id
