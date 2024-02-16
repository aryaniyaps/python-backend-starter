from typing import Annotated

from argon2 import PasswordHasher
from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
from geoip2.database import Reader
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repos import (
    AuthenticationTokenRepo,
    PasswordResetTokenRepo,
    UserSessionRepo,
)
from app.auth.services import AuthService
from app.auth.types import UserInfo
from app.core.database import get_database_session
from app.core.geo_ip import get_geoip_reader
from app.core.redis_client import get_redis_client
from app.core.security import get_password_hasher
from app.users.dependencies import get_email_verification_token_repo, get_user_repo
from app.users.repos import EmailVerificationTokenRepo, UserRepo

authentication_token_header = APIKeyHeader(name="X-Authentication-Token")


def get_authentication_token_repo(
    redis_client: Annotated[
        Redis,
        Depends(
            dependency=get_redis_client,
        ),
    ],
) -> AuthenticationTokenRepo:
    """Get the authentication token repo."""
    return AuthenticationTokenRepo(
        redis_client=redis_client,
    )


def get_password_reset_token_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
) -> PasswordResetTokenRepo:
    """Get the password reset token repo."""
    return PasswordResetTokenRepo(
        session=session,
    )


def get_user_session_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
    geoip_reader: Annotated[
        Reader,
        Depends(
            dependency=get_geoip_reader,
        ),
    ],
) -> UserSessionRepo:
    """Get the user session repo."""
    return UserSessionRepo(
        session=session,
        geoip_reader=geoip_reader,
    )


def get_auth_service(
    user_session_repo: Annotated[
        UserSessionRepo,
        Depends(
            dependency=get_user_session_repo,
        ),
    ],
    password_reset_token_repo: Annotated[
        PasswordResetTokenRepo,
        Depends(
            dependency=get_password_reset_token_repo,
        ),
    ],
    authentication_token_repo: Annotated[
        AuthenticationTokenRepo,
        Depends(
            dependency=get_authentication_token_repo,
        ),
    ],
    user_repo: Annotated[
        UserRepo,
        Depends(
            dependency=get_user_repo,
        ),
    ],
    email_verification_token_repo: Annotated[
        EmailVerificationTokenRepo,
        Depends(
            dependency=get_email_verification_token_repo,
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
        user_session_repo=user_session_repo,
        password_reset_token_repo=password_reset_token_repo,
        authentication_token_repo=authentication_token_repo,
        user_repo=user_repo,
        email_verification_token_repo=email_verification_token_repo,
        password_hasher=password_hasher,
        geoip_reader=geoip_reader,
    )


async def get_viewer_info(
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
) -> UserInfo:
    """Get the viewer (current user) info from the authentication token."""
    return await auth_service.get_user_info_for_authentication_token(
        authentication_token=authentication_token,
    )
