import pytest
from sanic import Sanic
from sanic_testing import TestManager
from sanic_testing.testing import SanicASGITestClient


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
