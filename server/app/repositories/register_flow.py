import secrets
import string
from hashlib import sha256
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.constants import REGISTER_FLOW_EXPIRES_IN
from app.models.register_flow import RegisterFlow


class RegisterFlowRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def generate_verification_code() -> str:
        """Generate an email verification code."""
        return "".join(secrets.choice(string.digits) for i in range(8))

    @staticmethod
    def hash_verification_code(email_verification_code: str) -> str:
        """Hash the given email verification code."""
        return sha256(email_verification_code.encode()).hexdigest()

    async def create(self, *, email: str) -> RegisterFlow:
        """Create a new register flow."""
        expires_at = text(
            f"NOW() + INTERVAL '{REGISTER_FLOW_EXPIRES_IN} SECOND'",
        )

        verification_code = self.generate_verification_code()

        # TODO: what about email verification code expiration

        register_flow = RegisterFlow(
            email=email,
            expires_at=expires_at,
            # hash code before storing
            verification_code_hash=self.hash_verification_code(
                email_verification_code=verification_code,
            ),
        )

        self._session.add(register_flow)
        await self._session.commit()
        return register_flow

    async def get(self, *, flow_id: UUID) -> RegisterFlow | None:
        """Get a register flow by ID."""
        return await self._session.scalar(
            select(RegisterFlow).where(RegisterFlow.id == flow_id),
        )

    async def update(
        self,
        register_flow: RegisterFlow,
        *,
        is_verified: bool | None = None,
    ) -> None:
        """Update the given register flow."""
        if is_verified is not None:
            register_flow.is_verified = is_verified

        self._session.add(register_flow)
        await self._session.commit()
