from typing import AsyncIterator

import pytest
from di import Container
from di.dependent import Dependent
from di.executors import AsyncExecutor

from app.auth.services import AuthService
from app.core.containers import DIScope
from app.users.services import UserService


@pytest.fixture
async def auth_service(test_container: Container) -> AsyncIterator[AuthService]:
    """Get the authentication service."""
    async with test_container.enter_scope(DIScope.REQUEST) as state:
        yield await test_container.solve(
            Dependent(AuthService),
            scopes=[
                DIScope.REQUEST,
            ],
        ).execute_async(
            executor=AsyncExecutor(),
            state=state,
        )


@pytest.fixture
async def user_service(test_container: Container) -> AsyncIterator[UserService]:
    """Get the user service."""
    async with test_container.enter_scope(DIScope.REQUEST) as state:
        yield await test_container.solve(
            Dependent(UserService),
            scopes=[
                DIScope.REQUEST,
            ],
        ).execute_async(
            executor=AsyncExecutor(),
            state=state,
        )
