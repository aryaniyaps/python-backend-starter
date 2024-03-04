from http import HTTPMethod

from ratelimit import Rule
from ratelimit.backends.redis import RedisBackend
from redis.asyncio import StrictRedis

from app.config import settings
from app.utils.regex_patterns import UUID_REGEX

rate_limit_backend = RedisBackend(
    StrictRedis.from_url(
        url=str(settings.redis_url),
    ),
)

# TODO: add rate limits for email change routes once the API is stable

rate_limit_config = {
    rf"/auth/register/flows/{UUID_REGEX.pattern}": [
        Rule(
            method=HTTPMethod.GET,
            hour=500,
            group="default",
        ),
    ],
    r"^/auth/register/flows/start": [
        Rule(
            method=HTTPMethod.POST,
            hour=75,
            group="default",
        ),
    ],
    rf"/auth/register/flows/{UUID_REGEX.pattern}/cancel": [
        Rule(
            method=HTTPMethod.POST,
            hour=75,
            group="default",
        ),
    ],
    rf"/auth/register/flows/{UUID_REGEX.pattern}/resend-verification": [
        Rule(
            method=HTTPMethod.POST,
            hour=75,
            group="default",
        ),
    ],
    rf"/auth/register/flows/{UUID_REGEX.pattern}/verify": [
        Rule(
            method=HTTPMethod.POST,
            hour=75,
            group="default",
        ),
    ],
    rf"/auth/register/flows/{UUID_REGEX.pattern}/webauthn-start": [
        Rule(
            method=HTTPMethod.POST,
            hour=75,
            group="default",
        ),
    ],
    rf"/auth/register/flows/{UUID_REGEX.pattern}/webauthn-finish": [
        Rule(
            method=HTTPMethod.POST,
            hour=75,
            group="default",
        ),
    ],
    r"/auth/logout": [
        Rule(
            method=HTTPMethod.POST,
            hour=250,
            group="default",
        ),
    ],
    r"/users/@me": [
        Rule(
            method=HTTPMethod.GET,
            hour=1000,
            group="default",
        ),
        Rule(
            method=HTTPMethod.PATCH,
            hour=500,
            group="default",
        ),
    ],
    rf"/users/{UUID_REGEX.pattern}": [
        Rule(
            method=HTTPMethod.GET,
            hour=2500,
            group="default",
        ),
    ],
}
