from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int

    username: str

    email: str

    password: Annotated[
        str,
        Field(
            exclude=True,
        ),
    ]

    last_login_at: datetime

    created_at: datetime

    updated_at: datetime
