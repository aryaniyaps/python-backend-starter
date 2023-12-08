from typing import AsyncIterator

import pytest
from falcon.asgi import App
from falcon.testing import ASGIConductor, TestClient


@pytest.fixture(scope="session")
def test_client(app: App) -> TestClient:
    """Initialize the test client."""
    return TestClient(app)


@pytest.fixture
async def conductor(test_client: TestClient) -> AsyncIterator[ASGIConductor]:
    """Initialize the test conductor for the ASGI app."""
    async with test_client as conductor:
        yield conductor


@pytest.fixture(scope="session")
async def auth_test_client(app: App, authentication_token: str) -> TestClient:
    """Initialize an authenticated test client for testing."""
    return TestClient(
        app,
        headers={
            "X-Authentication-Token": authentication_token,
        },
    )


@pytest.fixture
async def auth_conductor(auth_test_client: TestClient) -> AsyncIterator[ASGIConductor]:
    """Initialize an authenticated test conductor for the ASGI app."""
    async with auth_test_client as conductor:
        yield conductor
