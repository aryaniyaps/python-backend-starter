from typing import Annotated

from argon2 import PasswordHasher
from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
from geoip2.database import Reader

from app.dependencies.authentication_token import get_authentication_token_repo
from app.dependencies.email_verification_token import get_email_verification_token_repo
from app.dependencies.password_reset_token import get_password_reset_token_repo
from app.dependencies.user import get_user_repo
from app.dependencies.user_session import get_user_session_repo
from app.lib.geo_ip import get_geoip_reader
from app.lib.security import get_password_hasher
from app.repositories.authentication_token import AuthenticationTokenRepo
from app.repositories.email_verification_token import EmailVerificationTokenRepo
from app.repositories.password_reset_token import PasswordResetTokenRepo
from app.repositories.user import UserRepo
from app.repositories.user_session import UserSessionRepo
from app.services.auth import AuthService
from app.types.auth import UserInfo

authentication_token_header = APIKeyHeader(name="X-Authentication-Token")


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
