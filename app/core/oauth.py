from authlib.integrations.starlette_client import OAuth

from app.config import settings


def register_remote_apps(oauth_client: OAuth) -> None:
    """Register remote apps for the OAuth client."""
    oauth_client.register(
        "google",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile",
            "prompt": "select_account",  # force to select account
        },
    )


def create_oauth_client() -> OAuth:
    """Initialize an OAuth client."""
    oauth_client = OAuth()
    register_remote_apps(oauth_client)
    return oauth_client


oauth_client = create_oauth_client()
