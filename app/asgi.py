from sanic import Sanic
from uvicorn import Config, Server

from app.config import Settings


async def run_app(app: Sanic, settings: Settings) -> None:
    """Run the ASGI app instance."""
    server = Server(
        config=Config(
            app=app,
            host=settings.host,
            port=settings.port,
        ),
    )

    await server.serve()
