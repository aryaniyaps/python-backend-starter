import uvicorn

from app.config import settings
from app.logger import logging_config

if __name__ == "__main__":
    uvicorn.run(
        app="app:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        server_header=settings.debug,
        reload=settings.debug,
        log_config=logging_config,
        access_log=settings.debug,
    )
