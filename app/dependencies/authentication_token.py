from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from app.lib.redis_client import get_redis_client
from app.repositories.authentication_token import AuthenticationTokenRepo


def get_authentication_token_repo(
    redis_client: Annotated[
        Redis,
        Depends(
            dependency=get_redis_client,
        ),
    ],
) -> AuthenticationTokenRepo:
    """Get the authentication token repo."""
    return AuthenticationTokenRepo(
        redis_client=redis_client,
    )
