from typing import Annotated

from pydantic import Field

from app.core.schemas import BaseSchema


class HealthCheckResult(BaseSchema):
    status: Annotated[
        str,
        Field(
            examples=["OK"],
            description="The status of the application.",
        ),
    ]
