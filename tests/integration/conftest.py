from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app import create_app
from app.config import Settings
from app.core.database import get_database_connection
from tests.dependencies import get_test_database_connection


@pytest.fixture(scope="session")
def app(test_settings: Settings) -> FastAPI:
    """Initialize the app for testing."""
    app = create_app(settings=test_settings)
    setup_dependency_overrides(app)
    return app


def setup_dependency_overrides(app: FastAPI) -> None:
    """Setup dependency overrides for the app."""
    app.dependency_overrides[get_database_connection] = get_test_database_connection


@pytest.fixture
async def test_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Initialize a test client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture
async def auth_test_client(
    app: FastAPI, authentication_token: str
) -> AsyncGenerator[AsyncClient, None]:
    """Initialize an authenticated test client for testing."""
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={
            "X-Authentication-Token": authentication_token,
        },
    ) as auth_test_client:
        yield auth_test_client
