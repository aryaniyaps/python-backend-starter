from functools import lru_cache

from geoip2.database import Reader
from geoip2.models import City

from app.config import settings


def format_city_location(city: City) -> str:
    """Format the given GeoIP city to string."""
    return f"{city.city.name}, {city.subdivisions.most_specific.name} ({city.country.iso_code})"


@lru_cache
def get_geoip_reader() -> Reader:
    """Get the GeoIP database reader."""
    return Reader(settings.geolite2_database_path)
