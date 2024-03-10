from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

from app.lib.database.base import Base

CursorT = TypeVar("CursorT", UUID, bytes)

EntityT = TypeVar("EntityT", bound=Base)


@dataclass
class PagingInfo(Generic[CursorT]):
    after: CursorT | None
    limit: int


@dataclass
class PageInfo(Generic[CursorT]):
    """Additional metadata that aids in pagination."""

    has_next: bool
    start_cursor: CursorT | None


@dataclass
class Page(Generic[EntityT, CursorT]):
    """A paginated sequence of entities."""

    entities: list[EntityT]
    page_info: PageInfo[CursorT]
