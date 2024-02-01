from fastapi_sso.sso.google import GoogleSSO

from app.config import settings


def get_google_sso() -> GoogleSSO:
    """Get the Google SSO instance."""
    return GoogleSSO(
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
    )
