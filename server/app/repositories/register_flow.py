import secrets
import string
from hashlib import sha256
from uuid import UUID

from sqlalchemy import delete, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import now

from app.lib.constants import (
    EMAIL_VERIFICATION_CODE_EXPIRES_IN,
    REGISTER_FLOW_EXPIRES_IN,
)
from app.lib.enums import RegisterFlowStep
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

    async def create(
        self,
        *,
        email: str,
        ip_address: str,
        user_agent: str,
    ) -> tuple[str, RegisterFlow]:
        """Create a new register flow."""
        expires_at = text(
            f"NOW() + INTERVAL '{REGISTER_FLOW_EXPIRES_IN} SECOND'",
        )

        verification_code_expires_at = text(
            f"NOW() + INTERVAL '{EMAIL_VERIFICATION_CODE_EXPIRES_IN} SECOND'",
        )

        verification_code = self.generate_verification_code()

        register_flow = RegisterFlow(
            email=email,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at,
            verification_code_expires_at=verification_code_expires_at,
            # hash code before storing
            verification_code_hash=self.hash_verification_code(
                email_verification_code=verification_code,
            ),
        )

        self._session.add(register_flow)
        await self._session.commit()
        return verification_code, register_flow

    async def recreate_verification_code(
        self,
        *,
        flow_id: UUID,
    ) -> str:
        """Recreate the verification code for the register flow."""
        verification_code_expires_at = text(
            f"NOW() + INTERVAL '{EMAIL_VERIFICATION_CODE_EXPIRES_IN} SECOND'",
        )

        verification_code = self.generate_verification_code()

        await self._session.scalar(
            update(RegisterFlow)
            .where(RegisterFlow.id == flow_id)
            .values(
                verification_code_expires_at=verification_code_expires_at,
                verification_code_hash=self.hash_verification_code(
                    email_verification_code=verification_code,
                ),
            ),
        )

        return verification_code

    async def get(
        self, *, flow_id: UUID, step: RegisterFlowStep | None = None
    ) -> RegisterFlow | None:
        """
        Get a register flow by ID and/ or step.

        Filters expired register flows.
        """
        if step is not None:
            return await self._session.scalar(
                select(RegisterFlow).where(
                    RegisterFlow.id == flow_id
                    and RegisterFlow.current_step == step
                    and RegisterFlow.expires_at >= now()
                ),
            )
        return await self._session.scalar(
            select(RegisterFlow).where(
                RegisterFlow.id == flow_id and RegisterFlow.expires_at >= now()
            ),
        )

    async def update(
        self,
        register_flow: RegisterFlow,
        *,
        current_step: RegisterFlowStep | None = None,
    ) -> None:
        """Update the given register flow."""
        if current_step is not None:
            register_flow.current_step = current_step

        self._session.add(register_flow)
        await self._session.commit()

    async def delete(self, *, flow_id: UUID) -> None:
        """Delete a register flow by ID."""
        await self._session.execute(
            delete(RegisterFlow).where(RegisterFlow.id == flow_id),
        )
