from enum import Enum

# branding

SUPPORT_EMAIL = "support@example.com"

APP_NAME = "Starter"

APP_URL = "https://example.com"  # frontend app URL

# cookies

AUTHENTICATION_TOKEN_COOKIE = "authentication_token"  # noqa: S105

# email verification codes

EMAIL_VERIFICATION_CODE_EXPIRES_IN = 300  # 5 minutes

# register flows

REGISTER_FLOW_EXPIRES_IN = 1800  # 30 minutes

# webauthn challenges

WEBAUTHN_CHALLENGE_TTL = 300  # 5 minutes

# rate limiting

PRIMARY_RATE_LIMIT = "5000/hour"


# OpenAPI Tags


class OpenAPITag(Enum):
    """OpenAPI path operation tags."""

    USERS = "users"
    AUTHENTICATION = "authentication"
    HEALTH = "health"
    INTERNAL = "internal"
