from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field

from app.core.models import CoreModel


class User(CoreModel):
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
