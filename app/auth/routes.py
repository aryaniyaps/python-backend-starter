from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from app.auth.decorators import login_required
from app.auth.models import (
    LoginUserInput,
    LoginUserResult,
    RegisterUserInput,
    RegisterUserResult,
)
from app.auth.services import AuthService

auth_router = APIRouter(
    prefix="/auth",
)


@auth_router.post(
    "/register",
    response_model=RegisterUserResult,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    body: RegisterUserInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=AuthService,
        ),
    ],
) -> RegisterUserResult:
    """Register a new user."""
    return await auth_service.register_user(body)


@auth_router.post(
    "/login",
    response_model=LoginUserResult,
)
async def login_user(
    body: LoginUserInput,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=AuthService,
        ),
    ],
) -> LoginUserResult:
    """Login the current user."""
    return await auth_service.login_user(body)


@auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
@login_required
async def logout_user(
    request: Request,
    auth_service: Annotated[
        AuthService,
        Depends(
            dependency=AuthService,
        ),
    ],
) -> None:
    """Logout the current user."""
    current_user_id: UUID = request.state.current_user_id
    authentication_token: str = request.state.authentication_token
    await auth_service.remove_authentication_token(
        authentication_token=authentication_token,
        user_id=current_user_id,
    )
