from httpx_oauth.clients.google import GoogleOAuth2

from app.config import settings

google_oauth_client = GoogleOAuth2(
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
)
