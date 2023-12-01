from secrets import token_hex

from app.core.redis_client import redis_client
from app.users.models import User


class AuthRepo:
    @classmethod
    async def create_authentication_token(
        cls,
        user: User,
    ) -> str:
        """Create a new authentication token."""
        authentication_token = cls.generate_authentication_token()
        await redis_client.set(
            name=cls.generate_authentication_token_key(
                authentication_token=authentication_token,
            ),
            value=user.id,
        )
        return authentication_token

    @staticmethod
    def generate_authentication_token() -> str:
        """Generate an authentication token."""
        # Generate a random token
        return token_hex(32)

    @staticmethod
    def generate_authentication_token_key(authentication_token: str) -> str:
        """Generate a key for the authentication token."""
        return f"auth-token:${authentication_token}"

    @classmethod
    async def verify_authentication_token(
        cls,
        authentication_token: str,
    ) -> int | None:
        """
        Verify the given authentication token and
        return the corresponding user ID, if the token is valid.
        """
        user_id = await redis_client.get(
            name=cls.generate_authentication_token_key(
                authentication_token=authentication_token,
            )
        )
        return user_id

    @classmethod
    async def remove_authentication_tokens(cls, user_id: int) -> None:
        """
        Remove all the authentication tokens that
        exist for the given user ID.
        """
        raise NotImplementedError()

    @classmethod
    async def remove_authentication_token(cls, authentication_token: str) -> None:
        """Remove the given authentication token."""
        await redis_client.delete(
            cls.generate_authentication_token_key(
                authentication_token=authentication_token,
            ),
        )
