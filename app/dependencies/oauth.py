from typing import Annotated

from fastapi import Depends
from fastapi_sso.sso.google import GoogleSSO

from app.config import settings
from app.dependencies.user import get_user_repo
from app.repositories.user import UserRepo
from app.services.oauth import OAuthService


def get_oauth_service(
    user_repo: Annotated[
        UserRepo,
        Depends(
            dependency=get_user_repo,
        ),
    ],
) -> OAuthService:
    """Get the oauth service."""
    return OAuthService(
        user_repo=user_repo,
    )


def get_google_sso() -> GoogleSSO:
    """Get the Google SSO instance."""
    return GoogleSSO(
        client_id=settings.google_client_id.get_secret_value(),
        client_secret=settings.google_client_secret.get_secret_value(),
    )
