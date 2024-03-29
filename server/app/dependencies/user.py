from typing import Annotated

from fastapi import Depends
from geoip2.database import Reader
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.authentication_token import get_authentication_token_repo
from app.dependencies.database_session import get_database_session
from app.dependencies.email_verification_code import get_email_verification_code_repo
from app.dependencies.user_session import get_user_session_repo
from app.lib.geo_ip import get_geoip_reader
from app.repositories.authentication_token import AuthenticationTokenRepo
from app.repositories.email_verification_code import EmailVerificationCodeRepo
from app.repositories.user import UserRepo
from app.repositories.user_session import UserSessionRepo
from app.services.user import UserService


def get_user_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
) -> UserRepo:
    """Get the user repo."""
    return UserRepo(session=session)


def get_user_service(
    user_session_repo: Annotated[
        UserSessionRepo,
        Depends(
            dependency=get_user_session_repo,
        ),
    ],
    authentication_token_repo: Annotated[
        AuthenticationTokenRepo,
        Depends(
            dependency=get_authentication_token_repo,
        ),
    ],
    user_repo: Annotated[
        UserRepo,
        Depends(
            dependency=get_user_repo,
        ),
    ],
    email_verification_code_repo: Annotated[
        EmailVerificationCodeRepo,
        Depends(
            dependency=get_email_verification_code_repo,
        ),
    ],
    geoip_reader: Annotated[
        Reader,
        Depends(
            dependency=get_geoip_reader,
        ),
    ],
) -> UserService:
    """Get the user service."""
    return UserService(
        user_repo=user_repo,
        email_verification_code_repo=email_verification_code_repo,
        user_session_repo=user_session_repo,
        authentication_token_repo=authentication_token_repo,
        geoip_reader=geoip_reader,
    )
