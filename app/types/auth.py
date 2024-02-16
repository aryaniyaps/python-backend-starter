from typing import NamedTuple
from uuid import UUID


class UserInfo(NamedTuple):
    """User info associated with a particular authentication token."""

    user_id: UUID
    user_session_id: UUID
