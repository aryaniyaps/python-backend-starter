import aioredis

from app.config import settings


redis_client = aioredis.from_url(
    url=settings.redis_url,
)
