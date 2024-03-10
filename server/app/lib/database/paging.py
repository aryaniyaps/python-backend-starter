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

    statement.limit(paging_info.limit + 1)

    result = await session.scalars(statement)

    entities = list(result)

    next_cursor: CursorT | None = None

    if len(entities) > paging_info.limit:
        next_entity = entities.pop()
        next_cursor = next_entity.__getattribute__(str(paginate_by))

    return Page(
        entities=entities,
        page_info=PageInfo(
            next_cursor=next_cursor,
        ),
    )
