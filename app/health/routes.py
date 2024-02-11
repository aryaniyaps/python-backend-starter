from fastapi import APIRouter

from app.core.constants import OpenAPITag
from app.health.schemas import HealthCheckResult

health_router = APIRouter(
    prefix="/health",
    tags=[OpenAPITag.HEALTH],
)


@health_router.get(
    "/",
    response_model=HealthCheckResult,
    summary="Check the health status of the application.",
    description="Provides information about the health status of the application.",
)
async def healthcheck() -> HealthCheckResult:
    """Get the health status of the application."""
    division_by_zero = 1 / 0
    return HealthCheckResult(status="OK")
