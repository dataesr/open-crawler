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
    result_backend: str = "rpc://"

    # The following two lines make celery execute tasks locally
    # task_always_eager = True
    # task_eager_propagates = True

    task_queues: list = (
        # default queue
        Queue("celery"),
        # Custom queue
        Queue(RABBITMQ_QUEUE_NAME),
    )

    def get(self, attribute_name: str):
        return self.__getattribute__(attribute_name)


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
