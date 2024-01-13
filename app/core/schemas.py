from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


def _snake_to_camel(name: str) -> str:
    """Convert the given name from snake case to camel case."""
    first, *rest = name.split("_")
    return first + "".join(map(str.capitalize, rest))


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=_snake_to_camel,
        regex_engine="python-re",
    )


class ValidationError(BaseSchema):
    loc: Annotated[
        list[str] | None,
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


class ValidationErrorResult(BaseSchema):
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
        list[ValidationError],
        Field(
            description="A list of validation errors.",
        ),
    ]
