from enum import Enum

# Branding

SUPPORT_EMAIL = "support@example.com"

APP_NAME = "Starter"

APP_URL = "https://example.com"  # frontend app URL

# Password reset tokens

PASSWORD_RESET_TOKEN_EXPIRES_IN = 300  # 5 minutes

# Rate limiting

PRIMARY_RATE_LIMIT = "5000/hour"


# OpenAPI Tags


class OpenAPITag(Enum):
    """Enumeration representing tags used for OpenAPI path operations."""

    USERS = "users"
    AUTHENTICATION = "authentication"
    HEALTH = "health"
    INTERNAL = "internal"
