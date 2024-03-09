from app.schemas.base import BaseSchema

# TODO: make paging responses generic


class PageInfo(BaseSchema):
    has_previous_page: bool
    start_cursor: str | None
    has_next_page: bool
    end_cursor: str | None
