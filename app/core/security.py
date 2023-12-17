from argon2 import PasswordHasher


def get_password_hasher() -> PasswordHasher:
    """Get the password hasher."""
    return PasswordHasher()
