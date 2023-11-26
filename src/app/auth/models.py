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
