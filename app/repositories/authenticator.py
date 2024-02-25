from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.authenticator import Authenticator


class AuthenticatorRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: UUID,
        credential_id: str,
        credential_public_key: str,
        sign_count: int,
        credential_device_type: str,
        credential_backed_up: bool,
        transports: str | None,
    ) -> Authenticator:
        """Create a new authenticator."""
        authenticator = Authenticator(
            user_id=user_id,
            credential_id=credential_id,
            credential_public_key=credential_public_key,
            sign_count=sign_count,
            credential_device_type=credential_device_type,
            credential_backed_up=credential_backed_up,
            transports=transports,
        )
        self._session.add(authenticator)
        await self._session.commit()
        return authenticator
