import os
from functools import lru_cache

from kombu import Queue, Exchange


class BaseConfig:
    CRAWL_QUEUE_NAME = "crawl_queue"
    ACCESSIBILITY_QUEUE_NAME = "accessibility_queue"
    TECHNOLOGIES_QUEUE_NAME = "technologies_queue"
    GOOD_PRACTICES_QUEUE_NAME = "good_practices_queue"
    RESPONSIVENESS_QUEUE_NAME = "responsiveness_queue"
    CARBON_QUEUE_NAME = "carbon_footprint_queue"
    UPLOAD_QUEUE_NAME = "upload_queue"

    # MONGODB_HOST = "localhost"
    # MONGODB_PORT = 27017
    # MONGODB_DATABASE = "scanr_db"
    # MONGODB_COLLECTION = "scanr_html"

    result_backend: str = "redis://redis:6379"

    # The following two lines make celery execute tasks locally
    # task_always_eager = True
    # task_eager_propagates = True

    task_queues: tuple = (
        # default queue
        Queue("celery"),
        # Custom queues
        Queue(CRAWL_QUEUE_NAME, Exchange(CRAWL_QUEUE_NAME), routing_key=CRAWL_QUEUE_NAME),
        Queue(ACCESSIBILITY_QUEUE_NAME, Exchange(ACCESSIBILITY_QUEUE_NAME), routing_key=ACCESSIBILITY_QUEUE_NAME),
        Queue(TECHNOLOGIES_QUEUE_NAME, Exchange(TECHNOLOGIES_QUEUE_NAME), routing_key=TECHNOLOGIES_QUEUE_NAME),
        Queue(GOOD_PRACTICES_QUEUE_NAME, Exchange(GOOD_PRACTICES_QUEUE_NAME), routing_key=GOOD_PRACTICES_QUEUE_NAME),
        Queue(RESPONSIVENESS_QUEUE_NAME, Exchange(RESPONSIVENESS_QUEUE_NAME), routing_key=RESPONSIVENESS_QUEUE_NAME),
        Queue(CARBON_QUEUE_NAME, Exchange(CARBON_QUEUE_NAME), routing_key=CARBON_QUEUE_NAME),
        Queue(UPLOAD_QUEUE_NAME, Exchange(UPLOAD_QUEUE_NAME), routing_key=UPLOAD_QUEUE_NAME),
    )

    task_routes = {
        "crawl": {"queue": CRAWL_QUEUE_NAME, "routing_key": CRAWL_QUEUE_NAME},
        "get_accessibility": {"queue": ACCESSIBILITY_QUEUE_NAME, "routing_key": ACCESSIBILITY_QUEUE_NAME},
        "get_technologies": {"queue": TECHNOLOGIES_QUEUE_NAME, "routing_key": TECHNOLOGIES_QUEUE_NAME},
        "get_good_practices": {"queue": GOOD_PRACTICES_QUEUE_NAME, "routing_key": GOOD_PRACTICES_QUEUE_NAME},
        "get_responsiveness": {"queue": RESPONSIVENESS_QUEUE_NAME, "routing_key": RESPONSIVENESS_QUEUE_NAME},
        "get_carbon_footprint": {"queue": CARBON_QUEUE_NAME, "routing_key": CARBON_QUEUE_NAME},
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
