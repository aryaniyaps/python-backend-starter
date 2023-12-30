from fastapi import APIRouter

from app.core.constants import Tag
from app.meta.models import HealthCheckResult

meta_router = APIRouter(
    prefix="/meta",
    tags=[Tag.METADATA],
)


@meta_router.get(
    "/health",
    response_model=HealthCheckResult,
    summary="Check the health status of the application.",
    description="Provides information about the health status of the application.",
)
async def healthcheck() -> HealthCheckResult:
    """Get the health status of the application."""
    return HealthCheckResult(status="OK")
