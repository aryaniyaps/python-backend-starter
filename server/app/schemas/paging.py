from typing import Annotated, Generic, TypeVar

from pydantic import Field

from app.schemas.base import BaseSchema

EntityT = TypeVar("EntityT", bound=BaseSchema)

# TODO: use UUID as default for CursorT TypeVar after we upgrade to Python 3.13
# https://peps.python.org/pep-0696/

CursorT = TypeVar("CursorT")


class PageInfo(BaseSchema, Generic[CursorT]):
    next_cursor: Annotated[
        CursorT | None,
        Field(
            description="The cursor to continue pagination.",
        ),
    ]


class PaginatedResult(BaseSchema, Generic[EntityT, CursorT]):
    entities: Annotated[
        list[EntityT],
        Field(
            description="A list of entities.",
        ),
    ]

    page_info: Annotated[
        PageInfo[CursorT],
        Field(
            description="Information to aid in pagination.",
        ),
    ]
