from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr


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

    created_at: datetime

    updated_at: datetime
