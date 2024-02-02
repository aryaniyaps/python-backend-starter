from http import HTTPStatus

import pytest
from httpx import AsyncClient

pytestmark = [pytest.mark.anyio]


async def test_health(test_client: AsyncClient) -> None:
    """Ensure we can successfully retrieve application health information."""
    response = await test_client.get("/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "OK"}
