from functools import lru_cache

from geoip2.database import Reader

from app.config import settings


@lru_cache
def get_geoip_reader() -> Reader:
    """Get the GeoIP database reader."""
    return Reader(settings.geolite2_database_path)
