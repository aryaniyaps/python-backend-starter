import asyncio
from logging.config import dictConfig

from asgi_correlation_id import correlation_id
from saq import Job, Queue
from saq.types import Context
from saq.worker import Worker

from app.config import settings
from app.logger import build_worker_log_config, setup_logging
from app.sentry import setup_sentry
from app.tasks import (
    send_email_verification_request_email,
    send_new_login_device_detected_email,
    send_onboarding_email,
    send_password_reset_email,
    send_password_reset_request_email,
)


async def before_enqueue(job: Job) -> None:
    """
    Before enqueue handler.

    Sets the correlation ID for the job.
    """
    job.meta["request_id"] = correlation_id.get()


task_queue = Queue.from_url(
    url=str(settings.saq_broker_url),
)

task_queue.register_before_enqueue(
    callback=before_enqueue,
)


async def before_process(ctx: Context) -> None:
    """
    Before process handler.

    Loads the correlation ID from the enqueueing process.
    """
    request_id = ctx["job"].meta.get("request_id")
    correlation_id.set(request_id)


async def after_process(_ctx: Context) -> None:
    """
    After process handler.

    Resets the correlation ID for the process.
    """
    correlation_id.set(None)


if __name__ == "__main__":
    # set up logging
    setup_logging(
        human_readable=settings.debug,
    )

    dictConfig(
        build_worker_log_config(
            log_level=settings.log_level,
            human_readable=settings.debug,
        ),
    )

    # set up sentry
    setup_sentry()

    worker = Worker(
        queue=task_queue,
        functions=[
            send_password_reset_email,
            send_password_reset_request_email,
            send_new_login_device_detected_email,
            send_onboarding_email,
            send_email_verification_request_email,
        ],
        concurrency=settings.saq_concurrency,
        before_process=before_process,
        after_process=after_process,
    )

    # run worker
    asyncio.run(worker.start())
