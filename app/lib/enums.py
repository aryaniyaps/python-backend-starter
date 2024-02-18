from enum import StrEnum


class AuthProviderType(StrEnum):
    google = "google"
    email_password = "email_password"  # noqa: S105
