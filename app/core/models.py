from typing import Annotated, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


def _snake_to_camel(name: str) -> str:
    """Convert the given name from snake case to camel case."""
    first, *rest = name.split("_")
    return first + "".join(map(str.capitalize, rest))


class CoreModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=_snake_to_camel,
    )


class ValidationError(BaseModel):
    loc: List[str] | None = None
    msg: str
    type: str


class ValidationErrorResult(CoreModel):
    message: Annotated[
        str,
        Field(
            examples=[
                "Invalid input detected.",
            ],
        ),
    ]
    errors: List[ValidationError]
