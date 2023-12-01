from redis.asyncio import from_url

from app.config import settings

redis_client = from_url(
    url=str(settings.redis_url),
)
