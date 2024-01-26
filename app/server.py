import uvicorn

from app.config import settings
from app.logger import setup_logging

if __name__ == "__main__":
    setup_logging(
        log_level=settings.log_level,
    )
    uvicorn.run(
        app="app:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        server_header=settings.debug,
        reload=settings.debug,
        log_level=settings.log_level,
    )
