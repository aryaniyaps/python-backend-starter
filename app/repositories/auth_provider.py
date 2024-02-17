from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth_provider import AuthProvider, ProviderType


class AuthProviderRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: UUID,
        provider: ProviderType,
        provider_user_id: str,
    ) -> AuthProvider:
        """Create a new auth provider."""
        auth_provider = AuthProvider(
            user_id=user_id,
            provider=provider,
            provider_user_id=provider_user_id,
        )
        self._session.add(auth_provider)
        await self._session.commit()
        return auth_provider

    async def get(self, user_id: UUID, provider: ProviderType) -> AuthProvider | None:
        """Get the auth provider with the given provider and user ID."""
        return await self._session.scalar(
            select(AuthProvider).where(
                AuthProvider.user_id == user_id and AuthProvider.provider == provider
            ),
        )

    async def update(
        self,
        user_id: UUID,
        provider: ProviderType,
        password: str | None,
    ) -> None:
        """Update an auth provider."""
        raise NotImplementedError
