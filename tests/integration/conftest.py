from typing import AsyncIterator

import pytest
from di import Container
from sanic import Sanic
from sanic_testing import TestManager
from sanic_testing.testing import SanicASGITestClient

from app import create_app
from app.config import Settings
from app.core.containers import DIScope


@pytest.fixture(scope="session")
async def app(
    test_container: Container,
    test_settings: Settings,
) -> AsyncIterator[Sanic]:
    """Initialize the app for testing."""
    async with test_container.enter_scope(DIScope.APP) as app_state:
        yield create_app(
            settings=test_settings,
            container=test_container,
            app_state=app_state,
        )


@pytest.fixture
async def test_client(app: Sanic) -> SanicASGITestClient:
    """Initialize a test client for testing."""
    manager = TestManager(app=app)
    return manager.asgi_client


@pytest.fixture
async def auth_test_client(
    app: Sanic, authentication_token: str
) -> SanicASGITestClient:
    """Initialize an authenticated test client for testing."""
    manager = TestManager(app=app)

    asgi_client = manager.asgi_client
    asgi_client.headers = {
        "X-Authentication-Token": authentication_token,
    }
    return asgi_client
