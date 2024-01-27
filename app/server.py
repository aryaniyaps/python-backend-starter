import uvicorn

from app.config import settings
from app.logger import build_log_config, setup_logging

if __name__ == "__main__":
    # set up logging
    setup_logging(
        json_logs=(not settings.debug),
    )

    # run application
    uvicorn.run(
        app="app:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        server_header=settings.debug,
        reload=settings.debug,
        access_log=settings.debug,
        log_config=build_log_config(
            log_level=settings.log_level,
            json_logs=(not settings.debug),
        ),
    )
