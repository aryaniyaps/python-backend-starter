import re

_UUID_VERSION = "4"

_pattern = (
    "[a-f0-9]{8}-[a-f0-9]{4}-"
    + _UUID_VERSION
    + "[a-f0-9]{3}-"
    + "[89ab][a-f0-9]{3}-"
    + "[a-f0-9]{12}$"
)

UUID_REGEX = re.compile(
    _pattern,
    re.IGNORECASE,
)
