from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from app import create_app


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """Initialize the app for testing."""
    return create_app()


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
