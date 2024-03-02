import json
from pathlib import Path

from app import create_app
from fastapi.openapi.utils import get_openapi

openapi_schema_path = Path("../schema/openapi.json")

app = create_app()

openapi_content = get_openapi(
    title=app.title,
    version=app.version,
    openapi_version=app.openapi_version,
    description=app.description,
    routes=app.routes,
)

openapi_schema_path.write_text(json.dumps(openapi_content))
