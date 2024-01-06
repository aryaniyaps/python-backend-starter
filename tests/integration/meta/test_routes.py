import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = [pytest.mark.anyio]


async def test_health(test_client: AsyncClient) -> None:
    """Ensure we can successfully retrieve application health information."""
    response = await test_client.get("/meta/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}
