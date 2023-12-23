from typing import AsyncIterator

import pytest
from di import Container
from di.dependent import Dependent
from di.executors import AsyncExecutor

from app.auth.repos import AuthRepo
from app.core.containers import DIScope
from app.users.repos import UserRepo


@pytest.fixture
async def auth_repo(test_container: Container) -> AsyncIterator[AuthRepo]:
    """Get the authentication repository."""
    async with test_container.enter_scope(DIScope.REQUEST) as state:
        yield await test_container.solve(
            Dependent(AuthRepo),
            scopes=[
                DIScope.REQUEST,
            ],
        ).execute_async(
            executor=AsyncExecutor(),
            state=state,
        )


@pytest.fixture
async def user_repo(test_container: Container) -> AsyncIterator[UserRepo]:
    """Get the user repository."""
    async with test_container.enter_scope(DIScope.REQUEST) as state:
        yield await test_container.solve(
            Dependent(UserRepo),
            scopes=[
                DIScope.REQUEST,
            ],
        ).execute_async(
            executor=AsyncExecutor(),
            state=state,
        )
