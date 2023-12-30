from fastapi import APIRouter, status

from app.meta.models import HealthCheckResult

meta_router = APIRouter(
    prefix="/meta",
    tags=["metadata"],
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
