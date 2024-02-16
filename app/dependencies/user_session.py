from typing import Annotated

from fastapi import Depends
from geoip2.database import Reader
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.database import get_database_session
from app.lib.geo_ip import get_geoip_reader
from app.repositories.user_session import UserSessionRepo


def get_user_session_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
    geoip_reader: Annotated[
        Reader,
        Depends(
            dependency=get_geoip_reader,
        ),
    ],
) -> UserSessionRepo:
    """Get the user session repo."""
    return UserSessionRepo(
        session=session,
        geoip_reader=geoip_reader,
    )
