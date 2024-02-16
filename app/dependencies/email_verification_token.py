from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_database_session
from app.repositories.email_verification_token import EmailVerificationTokenRepo


def get_email_verification_token_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
) -> EmailVerificationTokenRepo:
    """Get the email verification token repo."""
    return EmailVerificationTokenRepo(
        session=session,
    )
