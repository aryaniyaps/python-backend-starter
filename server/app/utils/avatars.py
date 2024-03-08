import hashlib
import urllib

from app.lib.constants import GRAVATAR_DEFAULT_IMAGE, GRAVATAR_SIZE


def generate_avatar_url(email: str) -> str:
    """Generate a Gravatar URL for the user."""
    gravatar_url = (
        "https://www.gravatar.com/avatar/"
        + hashlib.md5(email.lower().encode("utf-8")).hexdigest()  # noqa: S324
        + "?"
    )
    gravatar_url += urllib.urlencode(
        {"d": GRAVATAR_DEFAULT_IMAGE, "s": str(GRAVATAR_SIZE)}
    )
    return gravatar_url
