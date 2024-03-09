from typing import Annotated

from fastapi import Query

from app.types.paging import PageInfo


def get_paging_info(
    limit: Annotated[
        int,
        Query(
            default=20,
            description="The amount of items to fetch.",
        ),
    ],
    after: Annotated[
        str | None,
        Query(
            default=None,
            description="The cursor after which items should be fetched.",
        ),
    ],
) -> None:
    """Get paging info from query parameters."""
    return PageInfo(limit=limit, after=after)
