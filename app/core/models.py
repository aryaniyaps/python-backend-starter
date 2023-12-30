from typing import Annotated, List

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


class ValidationError(CoreModel):
    loc: Annotated[
        List[str] | None,
        Field(
            default=None,
            description="The location of the validation error.",
        ),
    ]

    msg: Annotated[
        str,
        Field(
            description="A message describing the validation error.",
        ),
    ]

    type: Annotated[
        str,
        Field(
            description="The type of the validation error.",
        ),
    ]


class ValidationErrorResult(CoreModel):
    message: Annotated[
        str,
        Field(
            examples=[
                "Invalid input detected.",
            ],
            description="A human readable message describing the error.",
        ),
    ]
    errors: Annotated[
        List[ValidationError],
        Field(
            description="A list of validation errors.",
        ),
    ]
