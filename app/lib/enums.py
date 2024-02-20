from enum import StrEnum


class AuthProviderType(StrEnum):
    facebook = "facebook"
    google = "google"
    email_password = "email_password"  # noqa: S105
