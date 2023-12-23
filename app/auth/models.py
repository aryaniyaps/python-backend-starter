from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.users.models import User


class LoginUserInput(BaseModel):
    login: Annotated[
        str | EmailStr,
        Field(
            examples=[
                "aryaniyaps",
                "aryan@example.com",
            ],
        ),
    ]

    password: str


class LoginUserResult(BaseModel):
    authentication_token: str

    user: User


class RegisterUserInput(BaseModel):
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
            # TODO: fix regex issues with pydantic
            # pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=]).+",
        ),
    ]


class RegisterUserResult(BaseModel):
    authentication_token: str

    user: User


class PasswordResetRequestInput(BaseModel):
    email: Annotated[
        EmailStr,
        Field(
            max_length=250,
            examples=[
                "aryan@example.com",
            ],
        ),
    ]


class PasswordResetInput(BaseModel):
    email: Annotated[
        EmailStr,
        Field(
            max_length=250,
            examples=[
                "aryan@example.com",
            ],
        ),
    ]

    new_password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=32,
            # TODO: fix regex issues with pydantic
            # pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=]).+",
        ),
    ]

    reset_token: str


class PasswordResetToken(BaseModel):
    id: UUID

    user_id: UUID

    token_hash: Annotated[
        str,
        Field(
            exclude=True,
        ),
    ]

    last_login_at: datetime

    created_at: datetime

    expires_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
