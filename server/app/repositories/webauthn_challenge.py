import base64
from uuid import UUID

from redis.asyncio import Redis

from app.lib.constants import WEBAUTHN_CHALLENGE_TTL


class WebAuthnChallengeRepo:
    def __init__(self, redis_client: Redis) -> None:
        self._redis_client = redis_client

    @staticmethod
    def generate_challenge_key(challenge: bytes) -> str:
        """Generate a challenge key for the challenge."""
        challenge_base64 = base64.urlsafe_b64encode(challenge).decode("utf-8")
        return f"webauthn-challenges:{challenge_base64}"

    async def create(self, *, user_id: UUID, challenge: bytes) -> None:
        """Create a new WebAuthn challenge."""
        await self._redis_client.set(
            name=self.generate_challenge_key(
                challenge=challenge,
            ),
            value=user_id.bytes,
            ex=WEBAUTHN_CHALLENGE_TTL,
        )

    async def get(self, *, challenge: bytes) -> UUID | None:
        """Get the WebAuthn challenge user ID by challenge."""
        user_id = await self._redis_client.get(
            name=self.generate_challenge_key(
                challenge=challenge,
            ),
        )
        if user_id is not None:
            return UUID(bytes=user_id)
        return None

    async def delete(self, *, challenge: bytes) -> None:
        """Delete the given Webauthn challenge."""
        await self._redis_client.delete(
            self.generate_challenge_key(
                challenge=challenge,
            ),
        )
