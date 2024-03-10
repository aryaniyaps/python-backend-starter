from typing import Annotated

from fastapi import Query

from app.lib.constants import DEFAULT_PAGINATION_LIMIT, MAX_PAGINATION_LIMIT
from app.types.paging import PagingInfo


def get_paging_info(
    limit: Annotated[
        int,
        Query(
            description="The amount of entities to fetch.",
            le=MAX_PAGINATION_LIMIT,
        ),
    ] = DEFAULT_PAGINATION_LIMIT,
    after: Annotated[
        str | None,
        Query(
            description="The cursor after which entities should be fetched.",
        ),
    ] = None,
) -> PagingInfo:
    """Get paging info from query parameters."""
    return PagingInfo(limit=limit, after=after)
