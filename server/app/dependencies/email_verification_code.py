from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database_session import get_database_session
from app.repositories.email_verification_code import EmailVerificationCodeRepo


def get_email_verification_code_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
) -> EmailVerificationCodeRepo:
    """Get the email verification code repo."""
    return EmailVerificationCodeRepo(
        session=session,
    )
