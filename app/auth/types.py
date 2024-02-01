from typing import NamedTuple
from uuid import UUID


class UserInfo(NamedTuple):
    user_id: UUID
    user_session_id: UUID
