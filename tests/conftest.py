from typing import AsyncIterator
from falcon.asgi import App
from falcon.testing import TestClient, ASGIConductor
import pytest

from app import create_app


@pytest.fixture(scope="session")
def app() -> App:
    """Initialize the app for testing."""
    return create_app()


@pytest.fixture(scope="session")
def test_client(app: App) -> TestClient:
    """Initialize the test client."""
    return TestClient(app)


@pytest.fixture(scope="function")
async def conductor(test_client: TestClient) -> AsyncIterator[ASGIConductor]:
    async with test_client as conductor:
        yield conductor
