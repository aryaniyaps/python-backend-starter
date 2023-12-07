from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    id: UUID

    username: str

    email: str

    password_hash: Annotated[
        str,
        Field(
            exclude=True,
        ),
    ]

    last_login_at: datetime

    created_at: datetime

    updated_at: datetime
