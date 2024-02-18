from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.enums import AuthProviderType
from app.models.auth_provider import AuthProvider


class AuthProviderRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: UUID,
        provider: AuthProviderType,
    ) -> AuthProvider:
        """Create a new auth provider."""
        auth_provider = AuthProvider(
            user_id=user_id,
            provider=provider,
        )
        self._session.add(auth_provider)
        await self._session.commit()
        return auth_provider

    async def get(
        self, user_id: UUID, provider: AuthProviderType
    ) -> AuthProvider | None:
        """Get the auth provider with the given provider and user ID."""
        return await self._session.scalar(
            select(AuthProvider).where(
                AuthProvider.user_id == user_id and AuthProvider.provider == provider
            ),
        )

    async def update(
        self,
        user_id: UUID,
        provider: AuthProviderType,
        password: str | None,
    ) -> None:
        """Update an auth provider."""
        raise NotImplementedError
