from typing import Annotated, Literal

from pydantic import Field

from app.schemas.base import BaseSchema


class HealthCheckResult(BaseSchema):
    status: Annotated[
        Literal["OK"],
        Field(
            examples=["OK"],
            description="The status of the application.",
        ),
    ]
