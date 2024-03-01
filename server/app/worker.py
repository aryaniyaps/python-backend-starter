import asyncio
from logging.config import dictConfig

from asgi_correlation_id import correlation_id
from saq import CronJob, Job, Queue
from saq.types import Context
from saq.worker import Worker

from app.config import settings
from app.lib.database import get_database_session
from app.logger import build_worker_log_config, setup_logging
from app.tasks import (
    delete_expired_email_verification_codes,
    send_email_verification_request_email,
    send_new_login_device_detected_email,
    send_onboarding_email,
)


async def startup(ctx: Context) -> None:
    """
    Start up handler.

    Loads the database session into the context.
    """
    ctx["session"] = await get_database_session()


async def shutdown(ctx: Context) -> None:
    """
    Shutdown handler.

    Shuts down the existing database session.
    """
    await ctx["session"].close()


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

    worker = Worker(
        queue=task_queue,
        functions=[
            send_new_login_device_detected_email,
            send_onboarding_email,
            send_email_verification_request_email,
        ],
        cron_jobs=[
            CronJob(
                delete_expired_email_verification_codes,
                cron="0 * * * *",
            ),
        ],
        concurrency=settings.saq_concurrency,
        startup=startup,
        shutdown=shutdown,
        before_process=before_process,
        after_process=after_process,
    )

    # run worker
    asyncio.run(worker.start())
