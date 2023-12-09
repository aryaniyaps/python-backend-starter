from typing import Any

from celery import Task

from app.core.containers import container


class AioInjectTask(Task):
    abstract = True

    def __call__(self, *args, **kwargs) -> Any:
        with container.sync_context():
            return super().__call__(*args, **kwargs)
