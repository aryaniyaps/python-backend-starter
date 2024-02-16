from functools import lru_cache

from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError
from geoip2.models import City

from app.config import settings


def format_geoip_city(city: City) -> str:
    """Format the given GeoIP city to string."""
    return f"{city.city.name}, {city.subdivisions.most_specific.name} ({city.country.iso_code})"


def get_ip_location(ip_address: str, geoip_reader: Reader) -> str:
    """Get the location string from the given IP address."""
    try:
        city = geoip_reader.city(ip_address)
        return format_geoip_city(city)
    except AddressNotFoundError:
        return "Unknown"


@lru_cache
def get_geoip_reader() -> Reader:
    """Get the GeoIP database reader."""
    return Reader(settings.geolite2_database_path)
