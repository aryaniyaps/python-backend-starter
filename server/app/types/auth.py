from typing import NamedTuple
from uuid import UUID

from typing_extensions import TypedDict

from app.models.user import User


class UserInfo(NamedTuple):
    """User info associated with a particular authentication token."""

    user_id: UUID
    user_session_id: UUID


class AuthenticationResult(TypedDict):
    user: User
    authentication_token: str
