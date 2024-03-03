from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.database import get_database_session
from app.repositories.register_flow import RegisterFlowRepo


def get_register_flow_repo(
    session: Annotated[
        AsyncSession,
        Depends(
            dependency=get_database_session,
        ),
    ],
) -> RegisterFlowRepo:
    """Get the register flow repo."""
    return RegisterFlowRepo(session=session)
