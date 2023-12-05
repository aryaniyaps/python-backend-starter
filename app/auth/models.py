from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.users.models import User


class LoginUserInput(BaseModel):
    login: Annotated[
        str,
        Field(
            examples=[
                "aryaniyaps",
                "aryan@example.com",
            ],
        ),
    ]

    password: str

    @field_validator("login")
    @classmethod
    def validate_login(cls, value) -> EmailStr | str:
        """Validate the given login."""
        if "@" in value:
            # if "@" is present, assume it's an email
            return EmailStr(value)
        # assume it's an username
        return str(value)


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


class CreateUserResult(BaseModel):
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
    id: int

    user_id: int

    token_hash: Annotated[
        str,
        Field(
            exclude=True,
        ),
    ]

    last_login_at: datetime

    created_at: datetime

    expires_at: datetime
