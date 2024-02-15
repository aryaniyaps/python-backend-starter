from typing import Annotated

from argon2 import PasswordHasher
from fastapi import Depends
from geoip2.database import Reader
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_database_session
from app.core.geo_ip import get_geoip_reader
from app.core.security import get_password_hasher
from app.users.repos import UserRepo
from app.users.services import UserService


def get_user_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
    password_hasher: Annotated[
        PasswordHasher,
        Depends(
            dependency=get_password_hasher,
        ),
    ],
) -> UserRepo:
    """Get the user repo."""
    return UserRepo(
        session=session,
        password_hasher=password_hasher,
    )


def get_user_service(
    user_repo: Annotated[
        UserRepo,
        Depends(
            dependency=get_user_repo,
        ),
    ],
    password_hasher: Annotated[
        PasswordHasher,
        Depends(
            dependency=get_password_hasher,
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
        password_hasher=password_hasher,
        geoip_reader=geoip_reader,
    )
