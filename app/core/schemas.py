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


class ValidationErrorSchema(BaseSchema):
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


class UnexpectedErrorResult(BaseSchema):
    message: Annotated[
        str,
        Field(
            examples=[
                "An unexpected error occured.",
            ],
            description="A human readable message describing the error.",
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
        list[ValidationErrorSchema],
        Field(
            description="A list of validation errors.",
        ),
    ]


class HTTPExceptionResult(BaseSchema):
    message: Annotated[
        str,
        Field(
            examples=[
                "Invalid input detected.",
            ],
            description="A human readable message describing the error.",
        ),
    ]


class InvalidInputErrorResult(BaseSchema):
    message: Annotated[
        str,
        Field(
            examples=[
                "Invalid input detected.",
            ],
            description="A human readable message describing the error.",
        ),
    ]


class ResourceNotFoundErrorResult(BaseSchema):
    message: Annotated[
        str,
        Field(
            examples=[
                "Resource with ID 123 not found.",
            ],
            description="A human readable message describing the error.",
        ),
    ]


class UnauthenticatedErrorResult(BaseSchema):
    message: Annotated[
        str,
        Field(
            examples=[
                "Invalid authentication token provided.",
            ],
            description="A human readable message describing the error.",
        ),
    ]


class RateLimitExceededErrorResult(BaseSchema):
    message: Annotated[
        str,
        Field(
            examples=[
                "You are being ratelimited.",
            ],
            description="A human readable message describing the error.",
        ),
    ]

    is_primary: Annotated[
        bool,
        Field(
            title="Is Primary",
            description="Whether the primary rate limiter was exceeded.",
        ),
    ]
