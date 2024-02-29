from fastapi import APIRouter

from app.lib.constants import OpenAPITag
from app.schemas.health import HealthCheckResult

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
async def check_health() -> HealthCheckResult:
    """Get the health status of the application."""
    return HealthCheckResult(status="OK")
