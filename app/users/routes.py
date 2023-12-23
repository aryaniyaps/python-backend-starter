from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Request

from app.auth.decorators import login_required
from app.users.models import User
from app.users.services import UserService

users_router = APIRouter(
    prefix="/users",
)


@users_router.get("/@me", response_model=User)
@login_required
async def on_get_current_user(
    request: Request,
    user_service: Annotated[
        UserService,
        Depends(
            dependency=UserService,
        ),
    ],
) -> User:
    """Get the current user."""
    current_user_id: UUID = request.state.current_user_id
    return await user_service.get_user_by_id(
        user_id=current_user_id,
    )


@users_router.get("/{user_id}", response_model=User)
@login_required
async def on_get_user(
    user_id: Annotated[
        UUID,
        Path(
            title="The ID of the user to get.",
        ),
    ],
    user_service: Annotated[
        UserService,
        Depends(
            dependency=UserService,
        ),
    ],
) -> User:
    """Get the user with the given ID."""
    return await user_service.get_user_by_id(user_id=user_id)
