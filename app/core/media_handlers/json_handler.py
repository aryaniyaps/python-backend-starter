from functools import partial

import orjson
from falcon.media import JSONHandler

json_handler = JSONHandler(
    dumps=partial(
        orjson.dumps,
        option=orjson.OPT_NON_STR_KEYS,
    ),
    loads=orjson.loads,
)
