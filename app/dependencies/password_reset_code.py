from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.database import get_database_session
from app.repositories.password_reset_code import PasswordResetCodeRepo


def get_password_reset_code_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
) -> PasswordResetCodeRepo:
    """Get the password reset code repo."""
    return PasswordResetCodeRepo(
        session=session,
    )
