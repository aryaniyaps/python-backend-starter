from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.database import get_database_session
from app.repositories.webauthn_credential import WebAuthnCredentialRepo


def get_webauthn_credential_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
) -> WebAuthnCredentialRepo:
    """Get the WebAuthn credential repo."""
    return WebAuthnCredentialRepo(session=session)
