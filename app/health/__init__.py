from fastapi import APIRouter

from app.core.constants import OpenAPITag
from app.health.schemas import HealthCheckResult

health_router = APIRouter(
    prefix="/meta",
    tags=[OpenAPITag.METADATA],
)


@health_router.get(
    "/health",
    response_model=HealthCheckResult,
    summary="Check the health status of the application.",
    description="Provides information about the health status of the application.",
)
async def healthcheck() -> HealthCheckResult:
    """Get the health status of the application."""
    return HealthCheckResult(status="OK")
