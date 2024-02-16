from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.database import get_database_session
from app.repositories.password_reset_token import PasswordResetTokenRepo


def get_password_reset_token_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
) -> PasswordResetTokenRepo:
    """Get the password reset token repo."""
    return PasswordResetTokenRepo(
        session=session,
    )
