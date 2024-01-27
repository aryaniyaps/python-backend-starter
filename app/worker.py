from logging.config import dictConfig

from redis import Redis
from rq import Queue, Worker

from app.config import settings
from app.logger import build_log_config, setup_logging

task_queue = Queue(
    name="tasks",
    connection=Redis.from_url(
        url=str(
            settings.rq_broker_url,
        ),
    ),
)

if __name__ == "__main__":
    # set up logging
    setup_logging(
        json_logs=(not settings.debug),
    )
    dictConfig(
        build_log_config(
            log_level=settings.log_level,
            json_logs=(not settings.debug),
        ),
    )

    # run worker
    worker = Worker(
        queues=[
            task_queue,
        ],
        connection=Redis.from_url(
            url=str(
                settings.rq_broker_url,
            ),
        ),
    )

    worker.work()
