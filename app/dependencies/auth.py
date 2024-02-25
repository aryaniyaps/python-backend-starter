from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
from geoip2.database import Reader

from app.dependencies.auth_provider import get_auth_provider_repo
from app.dependencies.authentication_token import get_authentication_token_repo
from app.dependencies.authenticator import get_authenticator_repo
from app.dependencies.email_verification_code import get_email_verification_code_repo
from app.dependencies.user import get_user_repo
from app.dependencies.user_session import get_user_session_repo
from app.lib.geo_ip import get_geoip_reader
from app.repositories.auth_provider import AuthProviderRepo
from app.repositories.authentication_token import AuthenticationTokenRepo
from app.repositories.authenticator import AuthenticatorRepo
from app.repositories.email_verification_code import EmailVerificationCodeRepo
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
    authenticator_repo: Annotated[
        AuthenticatorRepo,
        Depends(
            dependency=get_authenticator_repo,
        ),
    ],
    auth_provider_repo: Annotated[
        AuthProviderRepo,
        Depends(
            dependency=get_auth_provider_repo,
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
        EmailVerificationCodeRepo,
        Depends(
            dependency=get_email_verification_code_repo,
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
        authenticator_repo=authenticator_repo,
        auth_provider_repo=auth_provider_repo,
        authentication_token_repo=authentication_token_repo,
        user_repo=user_repo,
        email_verification_code_repo=email_verification_token_repo,
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
