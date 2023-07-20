import os
from functools import lru_cache

from kombu import Queue, Exchange


class BaseConfig:
    CRAWL_QUEUE_NAME = "crawl_queue"
    UPLOAD_QUEUE_NAME = "upload_queue"

    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DATABASE = "scanr_db"
    MONGODB_COLLECTION = "scanr_html"

    result_backend: str = "rpc://"

    # The following two lines make celery execute tasks locally
    # task_always_eager = True
    # task_eager_propagates = True

    task_queues: list = (
        # default queue
        Queue("celery"),
        # Custom queues
        Queue(CRAWL_QUEUE_NAME, Exchange(CRAWL_QUEUE_NAME), routing_key=CRAWL_QUEUE_NAME),
        Queue(UPLOAD_QUEUE_NAME, Exchange(UPLOAD_QUEUE_NAME), routing_key=UPLOAD_QUEUE_NAME),
    )

    task_routes = {
        "crawl": {"queue": CRAWL_QUEUE_NAME, "routing_key": CRAWL_QUEUE_NAME},
        "upload_html": {"queue": UPLOAD_QUEUE_NAME, "routing_key": UPLOAD_QUEUE_NAME},
    }

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
