from redis.asyncio import Redis


class WebAuthnChallengeRepo:
    def __init__(self, redis_client: Redis) -> None:
        self._redis_client = redis_client

    async def create(self, *, username: str, challenge: bytes) -> None:
        """Create a new WebAuthn challenge."""
        await self._redis_client.set(
            name=self.generate_challenge_owner_key(
                username=username,
            ),
            value=challenge,
        )

    async def get(self, *, username: str) -> bytes | None:
        """Get WebAuthn challenge by username."""
        return await self._redis_client.get(
            name=self.generate_challenge_owner_key(
                username=username,
            ),
        )

    @staticmethod
    def generate_challenge_owner_key(username: str) -> str:
        """Generate a challenge owner key for the user ID."""
        return f"webauthn-challenge-owners:${username}"
