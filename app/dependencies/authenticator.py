from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.database import get_database_session
from app.repositories.authenticator import AuthenticatorRepo


def get_authenticator_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
) -> AuthenticatorRepo:
    """Get the authenticator repo."""
    return AuthenticatorRepo(session=session)
