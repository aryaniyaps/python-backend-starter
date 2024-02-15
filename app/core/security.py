from argon2 import PasswordHasher
from zxcvbn_rs_py import zxcvbn

from app.core.constants import MIN_PASSWORD_ZXCVBN_SCORE


def get_password_hasher() -> PasswordHasher:
    """Get the password hasher."""
    return PasswordHasher()


def check_password_strength(password: str, username: str, email: str) -> bool:
    """
    Check the strength of the given password.

    Checks the strength of the given password with the other fields
    entered by the user in context (using the zxcvbn algorithm).
    """
    password_strength = zxcvbn(
        password=password,
        user_inputs=[username, email],
    )

    return password_strength.score >= MIN_PASSWORD_ZXCVBN_SCORE
