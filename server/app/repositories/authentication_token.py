from hashlib import sha256
from secrets import token_hex
from uuid import UUID

from redis.asyncio import Redis

from app.types.auth import UserInfo


class AuthenticationTokenRepo:
    def __init__(self, redis_client: Redis) -> None:
        self._redis_client = redis_client

    async def create(
        self,
        user_id: UUID,
        user_session_id: UUID,
    ) -> str:
        """Create a new authentication token."""
        authentication_token = self.generate_token()
        # hash authentication token before storing
        authentication_token_hash = self.hash_token(
            authentication_token=authentication_token,
        )
        await self._redis_client.hset(
            name=self.generate_token_key(
                authentication_token_hash=authentication_token_hash,
            ),
            mapping={
                "user_id": user_id.bytes,
                "user_session_id": user_session_id.bytes,
            },
        )  # type: ignore[misc]
        await self._redis_client.sadd(
            self.generate_token_owner_key(
                user_id=user_id,
            ),
            authentication_token_hash,
        )  # type: ignore[misc]
        return authentication_token

    @staticmethod
    def generate_token() -> str:
        """Generate an authentication token."""
        return token_hex(32)

    @staticmethod
    def generate_token_key(authentication_token_hash: str) -> str:
        """Generate a token key for the authentication token hash."""
        return f"auth-tokens:${authentication_token_hash}"

    @staticmethod
    def generate_token_owner_key(user_id: UUID) -> str:
        """Generate a token owner key for the user ID."""
        return f"auth-token-owners:${user_id}"

    @staticmethod
    def hash_token(authentication_token: str) -> str:
        """Hash the given authentication token."""
        return sha256(authentication_token.encode()).hexdigest()

    async def get_user_info(
        self,
        authentication_token: str,
    ) -> UserInfo | None:
        """Get the user ID and user session ID for the authentication token."""
        user_info = await self._redis_client.hgetall(
            name=self.generate_token_key(
                authentication_token_hash=self.hash_token(
                    authentication_token=authentication_token,
                ),
            ),
        )  # type: ignore[misc]
        if user_info is not None:
            return UserInfo(
                user_id=UUID(
                    bytes=user_info.get("user_id"),
                ),
                user_session_id=UUID(
                    bytes=user_info.get("user_session_id"),
                ),
            )
        return None

    async def delete(
        self,
        authentication_token: str,
        user_id: UUID,
    ) -> None:
        """Delete the given authentication token."""
        authentication_token_hash = self.hash_token(
            authentication_token=authentication_token,
        )
        await self._redis_client.delete(authentication_token_hash)
        await self._redis_client.srem(
            self.generate_token_owner_key(
                user_id=user_id,
            ),
            authentication_token_hash,
        )  # type: ignore[misc]

    async def delete_all(
        self,
        user_id: UUID,
    ) -> None:
        """Delete all authentication tokens for the given user ID."""
        authentication_token_hashes = await self._redis_client.smembers(
            name=self.generate_token_owner_key(
                user_id=user_id,
            ),
        )  # type: ignore[misc]
        if authentication_token_hashes:
            await self._redis_client.delete(
                *[
                    self.generate_token_key(
                        authentication_token_hash=authentication_token_hash,
                    )
                    for authentication_token_hash in authentication_token_hashes
                ]
            )
        await self._redis_client.delete(
            self.generate_token_owner_key(
                user_id=user_id,
            ),
        )
