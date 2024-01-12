from typing import Annotated
from uuid import UUID

from argon2 import PasswordHasher
from fastapi import Depends, Header
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repos import AuthRepo
from app.auth.services import AuthService
from app.core.database import get_database_session
from app.core.errors import UnauthenticatedError
from app.core.redis_client import get_redis_client
from app.core.security import get_password_hasher
from app.users.dependencies import get_user_repo
from app.users.repos import UserRepo


def get_auth_repo(
    session: AsyncSession = Depends(
        dependency=get_database_session,
    ),
    redis_client: Redis = Depends(
        dependency=get_redis_client,
    ),
) -> AuthRepo:
    """Get the auth repo."""
    return AuthRepo(
        session=session,
        redis_client=redis_client,
    )


def get_auth_service(
    auth_repo: AuthRepo = Depends(
        dependency=get_auth_repo,
    ),
    user_repo: UserRepo = Depends(
        dependency=get_user_repo,
    ),
    password_hasher: PasswordHasher = Depends(
        dependency=get_password_hasher,
    ),
) -> AuthService:
    """Get the auth service."""
    return AuthService(
        auth_repo=auth_repo,
        user_repo=user_repo,
        password_hasher=password_hasher,
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
    return await auth_service.verify_authentication_token(
        authentication_token=authentication_token,
    )
