from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.database import get_database_session
from app.repositories.auth_provider import AuthProviderRepo


def get_auth_provider_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
) -> AuthProviderRepo:
    """Get the auth provider repo."""
    return AuthProviderRepo(session=session)
