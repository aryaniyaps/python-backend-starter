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

# password reset tokens

PASSWORD_RESET_TOKEN_EXPIRES_IN = 300  # 5 minutes

# email verification tokens

EMAIL_VERIFICATION_TOKEN_EXPIRES_IN = 600  # 10 minutes

# rate limiting

PRIMARY_RATE_LIMIT = "5000/hour"

# password strength

# ZXCVBN algorithm score ranges from 0 - 4 as follows:

# 0 too guessable: risky password. (guesses < 10^3)
# 1 very guessable: protection from throttled online attacks. (guesses < 10^6)
# 2 somewhat guessable: protection from unthrottled online attacks. (guesses < 10^8)
# 3 safely unguessable: moderate protection from offline slow-hash scenario. (guesses < 10^10)
# 4 very unguessable: strong protection from offline slow-hash scenario. (guesses >= 10^10)

MIN_PASSWORD_ZXCVBN_SCORE = 3


# OpenAPI Tags


class OpenAPITag(Enum):
    """OpenAPI path operation tags."""

    USERS = "users"
    AUTHENTICATION = "authentication"
    HEALTH = "health"
    INTERNAL = "internal"
