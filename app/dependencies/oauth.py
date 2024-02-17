from typing import Annotated

from fastapi import Depends
from fastapi_sso.sso.google import GoogleSSO
from geoip2.database import Reader

from app.config import settings
from app.dependencies.authentication_token import get_authentication_token_repo
from app.dependencies.user import get_user_repo
from app.dependencies.user_session import get_user_session_repo
from app.lib.geo_ip import get_geoip_reader
from app.repositories.authentication_token import AuthenticationTokenRepo
from app.repositories.user import UserRepo
from app.repositories.user_session import UserSessionRepo
from app.services.oauth import OAuthService


def get_oauth_service(
    user_repo: Annotated[
        UserRepo,
        Depends(
            dependency=get_user_repo,
        ),
    ],
    authentication_token_repo: Annotated[
        AuthenticationTokenRepo,
        Depends(
            dependency=get_authentication_token_repo,
        ),
    ],
    user_session_repo: Annotated[
        UserSessionRepo,
        Depends(
            dependency=get_user_session_repo,
        ),
    ],
    geoip_reader: Annotated[
        Reader,
        Depends(
            dependency=get_geoip_reader,
        ),
    ],
) -> OAuthService:
    """Get the oauth service."""
    return OAuthService(
        user_repo=user_repo,
        authentication_token_repo=authentication_token_repo,
        user_session_repo=user_session_repo,
        geoip_reader=geoip_reader,
    )


def get_google_sso() -> GoogleSSO:
    """Get the Google SSO instance."""
    return GoogleSSO(
        client_id=settings.google_client_id.get_secret_value(),
        client_secret=settings.google_client_secret.get_secret_value(),
    )
