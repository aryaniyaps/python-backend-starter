from enum import Enum

# branding

SUPPORT_EMAIL = "support@example.com"

APP_NAME = "Starter"

APP_URL = "https://example.com"  # frontend app URL

# usernames

# note: if this value is changed, the database migrations
# should be updated

MAX_USERNAME_LENGTH = 32

MIN_USERNAME_LENGTH = 2

# email verification codes

EMAIL_VERIFICATION_CODE_EXPIRES_IN = 600  # 10 minutes

# rate limiting

PRIMARY_RATE_LIMIT = "5000/hour"


# OpenAPI Tags


class OpenAPITag(Enum):
    """OpenAPI path operation tags."""

    USERS = "users"
    AUTHENTICATION = "authentication"
    HEALTH = "health"
    INTERNAL = "internal"
