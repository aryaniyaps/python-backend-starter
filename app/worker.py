from redis import Redis
from rq import Queue, Worker

from app.config import settings

task_queue = Queue(
    name="tasks",
    connection=Redis.from_url(
        url=str(
            settings.rq_broker_url,
        ),
    ),
)

if __name__ == "__main__":
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
