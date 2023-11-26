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


class CreateUserInput(BaseModel):
    username: Annotated[
        str,
        Field(
            max_length=32,
            min_length=2,
            examples=[
                "aryaniyaps",
            ],
        ),
    ]

    email: Annotated[
        EmailStr,
        Field(
            max_length=250,
            examples=[
                "aryan@example.com",
            ],
        ),
    ]

    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=32,
            pattern="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])$",
        ),
    ]


class CreateUserResult(BaseModel):
    authentication_token: str

    user: User
