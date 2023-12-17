from falcon.asgi import App
from uvicorn import Config, Server

from app.config import Settings


async def run_app(app: App, settings: Settings) -> None:
    """Run the ASGI app instance."""
    server = Server(
        config=Config(
            app=app,
            host=settings.host,
            port=settings.port,
        ),
    )

    await server.serve()
