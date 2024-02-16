from functools import lru_cache

from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError
from geoip2.models import City

from app.config import settings


def format_geoip_city(city: City) -> str:
    """Format the given GeoIP city to string."""
    return f"{city.city.name}, {city.subdivisions.most_specific.name} ({city.country.iso_code})"


def get_geoip_city(ip_address: str, geoip_reader: Reader) -> City | None:
    """Get the GeoIP city from the given IP address."""
    try:
        return geoip_reader.city(ip_address)
    except AddressNotFoundError:
        return None


def get_city_location(city: City | None) -> str:
    """Get the location string from the given city."""
    if city is None:
        return "Unknown"
    return format_geoip_city(city)


def get_city_subdivision_geoname_id(city: City | None) -> int | None:
    """Get the most specific subdivision's geoname ID from the given city."""
    if city is not None:
        return city.subdivisions.most_specific.geoname_id
    return None


@lru_cache
def get_geoip_reader() -> Reader:
    """Get the GeoIP database reader."""
    return Reader(settings.geolite2_database_path)
