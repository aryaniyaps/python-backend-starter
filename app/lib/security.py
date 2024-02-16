from typing import TypedDict

from argon2 import PasswordHasher
from zxcvbn_rs_py import zxcvbn

from app.lib.constants import MIN_PASSWORD_ZXCVBN_SCORE


def get_password_hasher() -> PasswordHasher:
    """Get the password hasher."""
    return PasswordHasher()


class PasswordStrengthContext(TypedDict):
    """
    Password strength context.

    Context to consider while checking password strength.
    """

    email: str
    username: str


def check_password_strength(password: str, context: PasswordStrengthContext) -> bool:
    """
    Check the strength of the given password.

    Checks the strength of the given password with the other fields
    entered by the user in context (using the zxcvbn algorithm).
    """
    return (
        zxcvbn(
            password=password,
            user_inputs=[
                context["username"],
                context["email"],
            ],
        ).score
        >= MIN_PASSWORD_ZXCVBN_SCORE
    )
