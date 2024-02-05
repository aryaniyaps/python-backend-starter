from typing import Annotated

from fastapi import Depends
from fastapi_sso.sso.google import GoogleSSO

from app.auth.dependencies import get_auth_repo
from app.auth.repos import AuthRepo
from app.config import settings
from app.oauth.services import OAuthService
from app.users.dependencies import get_user_repo
from app.users.repos import UserRepo


def get_oauth_service(
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
) -> OAuthService:
    """Get the oauth service."""
    return OAuthService(
        auth_repo=auth_repo,
        user_repo=user_repo,
    )


def get_google_sso() -> GoogleSSO:
    """Get the Google SSO instance."""
    return GoogleSSO(
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
    )
