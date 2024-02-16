from fastapi_sso import OpenID
from user_agents.parsers import UserAgent

from app.repositories.user import UserRepo


class OAuthService:
    def __init__(
        self,
        user_repo: UserRepo,
    ) -> None:
        self._user_repo = user_repo

    async def login_or_register_user(
        self,
        openid_user: OpenID,
        request_ip: str,
        user_agent: UserAgent,
    ) -> None:
        """Login or register the user associated with the given OpenID credentials."""
        if openid_user.email is None:
            # raise error
            pass
        if openid_user.display_name is None:
            # raise error
            pass
