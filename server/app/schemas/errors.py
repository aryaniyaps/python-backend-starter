from typing import Annotated

from pydantic import Field

from app.schemas.base import BaseSchema


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
                "An unexpected error occurred.",
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
