from typing import NamedTuple


class PageInfo(NamedTuple):
    """User info associated with a particular authentication token."""

    after: str | None
    limit: int
