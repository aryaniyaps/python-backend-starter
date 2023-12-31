from enum import Enum

# Branding

SUPPORT_EMAIL = "support@example.com"

APP_NAME = "Starter"

APP_URL = "https://example.com"  # frontend app URL

# Password reset tokens

PASSWORD_RESET_TOKEN_EXPIRES_IN = 300  # 5 minutes


# OpenAPI Tags


class OpenAPITag(Enum):
    """
    Enumeration representing tags used for
    OpenAPI path operations.
    """

    USERS = "users"
    AUTHENTICATION = "authentication"
    METADATA = "metadata"
