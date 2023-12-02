from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings

engine = create_async_engine(
    url=str(settings.database_url),
    echo=settings.debug,
)

database_metadata = MetaData()