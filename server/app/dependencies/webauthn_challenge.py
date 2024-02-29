from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from app.lib.redis_client import get_redis_client
from app.repositories.webauthn_challenge import WebAuthnChallengeRepo


def get_webauthn_challenge_repo(
    redis_client: Annotated[
        Redis,
        Depends(
            dependency=get_redis_client,
        ),
    ],
) -> WebAuthnChallengeRepo:
    """Get the WebAuthn challenge repo."""
    return WebAuthnChallengeRepo(
        redis_client=redis_client,
    )
