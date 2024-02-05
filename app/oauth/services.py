from fastapi_sso import OpenID
from user_agents.parsers import UserAgent

from app.auth.repos import AuthRepo
from app.users.models import User
from app.users.repos import UserRepo


class OAuthService:
    def __init__(
        self,
        auth_repo: AuthRepo,
        user_repo: UserRepo,
    ) -> None:
        self._auth_repo = auth_repo
        self._user_repo = user_repo

    async def login_or_register_user(
        self,
        openid_user: OpenID,
        request_ip: str,
        user_agent: UserAgent,
    ) -> tuple[str, User]:
        """Login or register the user associated with the given OpenID credentials."""
        raise NotImplementedError
