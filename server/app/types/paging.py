from dataclasses import dataclass
from typing import Generic, TypeVar

from app.lib.database.base import Base

# TODO: use UUID as default for CursorT TypeVar after we upgrade to Python 3.13
# https://peps.python.org/pep-0696/

CursorT = TypeVar("CursorT")

EntityT = TypeVar("EntityT", bound=Base)


@dataclass
class PagingInfo(Generic[CursorT]):
    """Information required for pagination."""

    after: CursorT | None
    limit: int


@dataclass
class PageInfo(Generic[CursorT]):
    """Additional information that aids in pagination."""

    next_cursor: CursorT | None


@dataclass
class Page(Generic[EntityT, CursorT]):
    """A paginated sequence of entities."""

    entities: list[EntityT]
    page_info: PageInfo[CursorT]
