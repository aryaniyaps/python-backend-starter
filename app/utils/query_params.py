from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def append_query_param(url: str, param_name: str, param_value: str) -> str:
    """Append a query parameter to a URL."""
    parsed_url = urlparse(url)
    query_params = dict(parse_qsl(parsed_url.query))
    query_params[param_name] = param_value
    encoded_query = urlencode(query_params)
    return urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            encoded_query,
            parsed_url.fragment,
        )
    )
