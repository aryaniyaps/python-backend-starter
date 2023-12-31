from typing import Annotated

from pydantic import Field

from app.core.models import CoreModel


class HealthCheckResult(CoreModel):
    status: Annotated[
        str,
        Field(
            examples=["OK"],
            description="The status of the application.",
        ),
    ]
