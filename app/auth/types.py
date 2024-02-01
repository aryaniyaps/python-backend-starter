from typing import NamedTuple
from uuid import UUID


class UserInfo(NamedTuple):
    user_id: UUID
    login_session_id: UUID
