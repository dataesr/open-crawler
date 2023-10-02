import os

from celery import Celery

from app.celery_broker.config import settings


def create_celery_app() -> Celery:
    celery_app = Celery(
        "scanr",
        broker=os.environ.get("CELERY_BROKER_URL"),
        backend=os.environ.get("CELERY_RESULT_BACKEND"),
        broker_connection_retry_on_startup=True,
        include=["app.celery_broker.tasks"],
    )
    celery_app.config_from_object(settings, namespace="CELERY")

    celery_config_updates = {
        "task_track_started": True,
        "task_serializer": "pickle",
        "result_serializer": "pickle",
        "accept_content": ["pickle", "json"],
        "result_persistent": True,
        "worker_send_task_events": True,
        "worker_prefetch_multiplier": 1,
    }
    celery_app.conf.update(celery_config_updates)

    return celery_app
