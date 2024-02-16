from datetime import datetime
from uuid import UUID

from geoip2.database import Reader
from sqlalchemy import ScalarResult, delete, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from user_agents.parsers import UserAgent

from app.lib.geo_ip import (
    get_city_location,
    get_city_subdivision_geoname_id,
    get_geoip_city,
)
from app.models.user_session import UserSession


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
        user_id: UUID,
        ip_address: str,
        user_agent: UserAgent,
    ) -> UserSession:
        """Create a new user session."""
        # TODO: pass device ID here, like instagram does on register/ login
        # TODO: check if we need to store user_agent, we seem to only need device here
        # TODO: can we rename subdivision_geoname_id to subdivision_id or location_subdivision_id?
        city = get_geoip_city(
            ip_address=ip_address,
            geoip_reader=self._geoip_reader,
        )
        user_session = UserSession(
            user_id=user_id,
            ip_address=ip_address,
            subdivision_geoname_id=get_city_subdivision_geoname_id(city),
            location=get_city_location(city),
            user_agent=str(user_agent),
            device=user_agent.device,
        )
        self._session.add(user_session)
        await self._session.commit()
        return user_session

    async def check_if_exists(
        self,
        user_id: UUID,
        user_agent: UserAgent,
        ip_address: str,
    ) -> bool:
        """Check whether user sessions for the user exist with the given user agent and IP address."""
        # TODO: pass device ID here, like instagram does on register/ login
        # TODO: handle case where subdivision_geoname_id is None
        subdivision_geoname_id = get_city_subdivision_geoname_id(
            city=get_geoip_city(
                ip_address=ip_address,
                geoip_reader=self._geoip_reader,
            ),
        )
        results = await self._session.scalars(
            select(UserSession).where(
                UserSession.user_id == user_id
                and UserSession.device == user_agent.device
                and UserSession.subdivision_geoname_id == subdivision_geoname_id
            ),
        )
        return results.first() is not None

    async def check_if_exists_after(self, user_id: UUID, timestamp: datetime) -> bool:
        """Check whether user sessions for the user which are created after the given timestamp exist."""
        results = await self._session.scalars(
            select(UserSession).where(
                UserSession.user_id == user_id and UserSession.created_at > timestamp
            ),
        )
        return results.first() is not None

    async def get_all(self, user_id: UUID) -> ScalarResult[UserSession]:
        """Get user sessions for the given user ID."""
        return await self._session.scalars(
            select(UserSession).where(
                UserSession.user_id == user_id,
            ),
        )

    async def delete(
        self,
        user_session_id: UUID,
        user_id: UUID,
    ) -> None:
        """Delete a user session."""
        await self._session.execute(
            delete(UserSession).where(
                UserSession.id == user_session_id and UserSession.user_id == user_id,
            ),
        )

    async def update(
        self,
        user_session_id: UUID,
        logged_out_at: datetime | None,
    ) -> None:
        """Delete a user session."""
        await self._session.execute(
            update(UserSession)
            .where(UserSession.id == user_session_id)
            .values(
                logged_out_at=logged_out_at,
            )
        )

    async def logout_all(
        self,
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
