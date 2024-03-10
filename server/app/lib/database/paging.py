from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from app.types.paging import CursorT, EntityT, Page, PageInfo, PagingInfo


async def paginate(
    *,
    session: AsyncSession,
    statement: Select[tuple[EntityT]],
    paginate_by: Mapped[CursorT],
    paging_info: PagingInfo[CursorT],
) -> Page[EntityT, CursorT]:
    """Paginate the given statement."""
    if paging_info.after is not None:
        statement.filter(paginate_by > paging_info.after)

    statement.limit(paging_info.limit)
    entities = await session.scalars(statement)

    return Page(
        entities=list(entities),
        page_info=PageInfo(
            has_next=True,
            start_cursor=None,
        ),
    )
