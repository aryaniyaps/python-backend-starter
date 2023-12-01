from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, validator

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

    @validator("login")
    @classmethod
    def validate_login(cls, value):
        if "@" in value:
            # if "@" is present, assume it's an email
            return EmailStr(value)
        # assume it's an username
        return value


class LoginUserResult(BaseModel):
    authentication_token: str

    user: User


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
            # TODO: fix regex issues with pydantic
            # pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=]).+",
        ),
    ]


class CreateUserResult(BaseModel):
    authentication_token: str

    user: User
