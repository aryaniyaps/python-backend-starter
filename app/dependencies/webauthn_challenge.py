from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.database import get_database_session
from app.repositories.webauthn_challenge import WebAuthnChallengeRepo


def get_webauthn_challenge_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
) -> WebAuthnChallengeRepo:
    """Get the WebAuthn challenge repo."""
    return WebAuthnChallengeRepo(session=session)
