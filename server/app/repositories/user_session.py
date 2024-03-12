from datetime import datetime
from uuid import UUID

from geoip2.database import Reader
from sqlalchemy import delete, desc, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from user_agents.parsers import UserAgent

from app.lib.database.paging import paginate
from app.lib.geo_ip import (
    get_city_location,
    get_geoip_city,
)
from app.models.user_session import UserSession
from app.types.paging import Page, PagingInfo


class UserSessionRepo:
    def __init__(
        self,
        session: AsyncSession,
        geoip_reader: Reader,
    ) -> None:
        self._session = session
        self._geoip_reader = geoip_reader

    async def create(
        self,
        *,
        user_id: UUID,
        webauthn_credential_id: UUID,
        ip_address: str,
        user_agent: UserAgent,
    ) -> UserSession:
        """Create a new user session."""
        user_session = UserSession(
            user_id=user_id,
            webauthn_credential_id=webauthn_credential_id,
            ip_address=ip_address,
            location=get_city_location(
                city=get_geoip_city(
                    ip_address=ip_address,
                    geoip_reader=self._geoip_reader,
                ),
            ),
            user_agent=str(user_agent),
        )
        self._session.add(user_session)
        await self._session.commit()
        return user_session

    async def get_all(
        self,
        *,
        user_id: UUID,
        paging_info: PagingInfo,
    ) -> Page[UserSession, UUID]:
        """Get user sessions for the given user ID."""
        statement = (
            select(UserSession)
            .where(
                UserSession.user_id == user_id,
            )
            .order_by(desc(UserSession.created_at))
        )

        return await paginate(
            session=self._session,
            statement=statement,
            paginate_by=UserSession.id,
            paging_info=paging_info,
        )

    async def delete(
        self,
        *,
        user_session_id: UUID,
        user_id: UUID,
    ) -> None:
        """Delete an user session."""
        await self._session.execute(
            delete(UserSession).where(
                UserSession.id == user_session_id and UserSession.user_id == user_id,
            ),
        )
        await self._session.commit()

    async def update(
        self,
        *,
        user_session_id: UUID,
        logged_out_at: datetime | None,
    ) -> None:
        """Update an user session."""
        await self._session.execute(
            update(UserSession)
            .where(UserSession.id == user_session_id)
            .values(
                logged_out_at=logged_out_at,
            )
        )
        await self._session.commit()

    async def logout_all(
        self,
        *,
        user_id: UUID,
    ) -> None:
        """Mark all user sessions with the given user ID as logged out."""
        await self._session.execute(
            update(UserSession)
            .where(UserSession.user_id == user_id)
            .values(
                logged_out_at=text("NOW()"),
            ),
        )
        await self._session.commit()
