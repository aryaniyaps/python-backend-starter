from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from webauthn.helpers.structs import AuthenticatorTransport

from app.models.webauthn_credential import WebAuthnCredential


class WebAuthnCredentialRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        credential_id: str,
        user_id: UUID,
        public_key: str,
        sign_count: int,
        device_type: str,
        backed_up: bool,
        transports: list[AuthenticatorTransport] | None,
    ) -> WebAuthnCredential:
        """Create a new WebAuthn credential."""
        webauthn_credential = WebAuthnCredential(
            user_id=user_id,
            id=credential_id,
            public_key=public_key,
            sign_count=sign_count,
            device_type=device_type,
            backed_up=backed_up,
            transports=transports,
        )
        self._session.add(webauthn_credential)
        await self._session.commit()
        return webauthn_credential

    async def get(self, credential_id: str) -> WebAuthnCredential:
        """Get WebAuthn credential by ID."""
        return await self._session.scalar(
            select(WebAuthnCredential).where(
                WebAuthnCredential.id == credential_id,
            ),
        )

    async def get_all(self, user_id: UUID) -> list[WebAuthnCredential]:
        """Get all WebAuthn credentials by user ID."""
        credentials = await self._session.scalars(
            select(WebAuthnCredential).where(
                WebAuthnCredential.user_id == user_id,
            ),
        )
        return list(credentials)
