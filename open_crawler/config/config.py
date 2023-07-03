import os
from functools import lru_cache

from kombu import Queue


class BaseConfig:
    RABBITMQ_HOST = "localhost"
    RABBITMQ_PORT = 5672
    RABBITMQ_USERNAME = "guest"
    RABBITMQ_PASSWORD = "guest"
    RABBITMQ_QUEUE_NAME = "scanr_queue"

    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DATABASE = "scanr_db"
    MONGODB_COLLECTION = "scanr_html"

    CELERY_BROKER_URL: str = f"pyamqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"
    CELERY_RESULT_BACKEND: str = "rpc://"

    # The following two lines make celery execute in the same thread as the currently executing thread.
    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

    CELERY_TASK_QUEUES: list = (
        # default queue
        Queue("celery"),
        # Custom queue
        Queue(RABBITMQ_QUEUE_NAME),
    )


class DevelopmentConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
    }
    config_name = os.environ.get("CELERY_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()

