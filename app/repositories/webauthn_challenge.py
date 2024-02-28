from uuid import UUID

from redis.asyncio import Redis

from app.lib.constants import WEBAUTHN_CHALLENGE_TTL


class WebAuthnChallengeRepo:
    def __init__(self, redis_client: Redis) -> None:
        self._redis_client = redis_client

    @staticmethod
    def generate_challenge_key(challenge: str) -> str:
        """Generate a challenge key for the challenge."""
        return f"webauthn-challenges:{challenge}"

    async def create(self, *, user_id: UUID, challenge: str) -> None:
        """Create a new WebAuthn challenge."""
        await self._redis_client.set(
            name=self.generate_challenge_key(
                challenge=challenge,
            ),
            value=user_id.bytes,
            ex=WEBAUTHN_CHALLENGE_TTL,
        )

    async def get(self, *, challenge: str) -> UUID | None:
        """Get the WebAuthn challenge user ID by challenge."""
        user_id = await self._redis_client.get(
            name=self.generate_challenge_key(
                challenge=challenge,
            ),
        )
        if user_id is not None:
            return UUID(bytes=user_id)
        return None

    async def delete(self, *, challenge: str) -> None:
        """Delete the given Webauthn challenge."""
        await self._redis_client.delete(
            self.generate_challenge_key(
                challenge=challenge,
            ),
        )
