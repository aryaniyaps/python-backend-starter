from typing import Annotated, Generic, TypeVar
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseSchema

EntityT = TypeVar("EntityT", bound=BaseSchema)

CursorT = TypeVar("CursorT", UUID, bytes)


class PageInfo(BaseSchema, Generic[CursorT]):
    start_cursor: Annotated[
        CursorT | None,
        Field(
            description="The cursor to continue pagination.",
        ),
    ]

    has_next_page: Annotated[
        bool,
        Field(
            description="When paginating, are there more entities?",
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
