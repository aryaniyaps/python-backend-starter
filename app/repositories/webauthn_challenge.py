from redis.asyncio import Redis

from app.lib.constants import WEBAUTHN_CHALLENGE_TTL


class WebAuthnChallengeRepo:
    def __init__(self, redis_client: Redis) -> None:
        self._redis_client = redis_client

    async def create(self, *, email: str, challenge: bytes) -> None:
        """Create a new WebAuthn challenge."""
        await self._redis_client.set(
            name=self.generate_challenge_owner_key(
                email=email,
            ),
            value=challenge,
            ex=WEBAUTHN_CHALLENGE_TTL,
        )

    async def get(self, *, email: str) -> bytes | None:
        """Get WebAuthn challenge by email."""
        return await self._redis_client.get(
            name=self.generate_challenge_owner_key(
                email=email,
            ),
        )

    @staticmethod
    def generate_challenge_owner_key(email: str) -> str:
        """Generate a challenge owner key for the user ID."""
        return f"webauthn-challenge-owners:${email}"
