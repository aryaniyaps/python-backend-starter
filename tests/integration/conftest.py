from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
from app import create_app
from app.core.database import get_database_session
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """Initialize the app for testing."""
    return create_app()


@pytest.fixture(autouse=True)
def setup_dependency_overrides(
    app: FastAPI,
    test_database_session: AsyncSession,
) -> None:
    """Setup dependency overrides for the application."""

    def get_test_database_session() -> Generator[AsyncSession, Any, None]:
        """Get the test database session."""
        yield test_database_session

    app.dependency_overrides[get_database_session] = get_test_database_session


@pytest.fixture
async def test_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Initialize a test client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture
async def auth_test_client(
    app: FastAPI,
    authentication_token: str,
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
