from datetime import datetime
from uuid import UUID

from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.lib.database.base import Base
from app.lib.enums import RegisterFlowStep


class RegisterFlow(Base):
    __tablename__ = "register_flows"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text(
            "gen_random_uuid()",
        ),
    )

    current_step: Mapped[RegisterFlowStep] = mapped_column(
        default=RegisterFlowStep.EMAIL_VERIFICATION,
    )

    email: Mapped[str] = mapped_column(
        CITEXT(250),
        index=True,
    )

    verification_code_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    verification_code_expires_at: Mapped[datetime]

    ip_address: Mapped[str] = mapped_column(
        String(40),
    )

    user_agent: Mapped[str]

    expires_at: Mapped[datetime]
