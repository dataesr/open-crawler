import os
from functools import lru_cache

from kombu import Queue, Exchange


class BaseConfig:
    CRAWL_QUEUE_NAME = "crawl_queue"
    LIGHTHOUSE_QUEUE_NAME = "lighthouse_queue"
    TECHNOLOGIES_QUEUE_NAME = "technologies_queue"
    RESPONSIVENESS_QUEUE_NAME = "responsiveness_queue"
    CARBON_QUEUE_NAME = "carbon_footprint_queue"

    # The following two lines make celery execute tasks locally
    # task_always_eager = True
    # task_eager_propagates = True

    task_queues: tuple = (
        # default queue
        Queue("celery"),
        # Custom queues
        Queue(
            CRAWL_QUEUE_NAME,
            Exchange(CRAWL_QUEUE_NAME),
            routing_key=CRAWL_QUEUE_NAME,
        ),
        Queue(
            LIGHTHOUSE_QUEUE_NAME,
            Exchange(LIGHTHOUSE_QUEUE_NAME),
            routing_key=LIGHTHOUSE_QUEUE_NAME,
        ),
        Queue(
            TECHNOLOGIES_QUEUE_NAME,
            Exchange(TECHNOLOGIES_QUEUE_NAME),
            routing_key=TECHNOLOGIES_QUEUE_NAME,
        ),
        Queue(
            RESPONSIVENESS_QUEUE_NAME,
            Exchange(RESPONSIVENESS_QUEUE_NAME),
            routing_key=RESPONSIVENESS_QUEUE_NAME,
        ),
        Queue(
            CARBON_QUEUE_NAME,
            Exchange(CARBON_QUEUE_NAME),
            routing_key=CARBON_QUEUE_NAME,
        ),
    )

    task_routes = {
        "crawl": {"queue": CRAWL_QUEUE_NAME, "routing_key": CRAWL_QUEUE_NAME},
        "get_lighthouse": {
            "queue": LIGHTHOUSE_QUEUE_NAME,
            "routing_key": LIGHTHOUSE_QUEUE_NAME,
        },
        "get_technologies": {
            "queue": TECHNOLOGIES_QUEUE_NAME,
            "routing_key": TECHNOLOGIES_QUEUE_NAME,
        },
        "get_responsiveness": {
            "queue": RESPONSIVENESS_QUEUE_NAME,
            "routing_key": RESPONSIVENESS_QUEUE_NAME,
        },
        "get_carbon_footprint": {
            "queue": CARBON_QUEUE_NAME,
            "routing_key": CARBON_QUEUE_NAME,
        }
    }

    def get(self, attribute_name: str):
        return self.__getattribute__(attribute_name)


class DevelopmentConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "default": BaseConfig
    }
    config_name = os.environ.get("CELERY_CONFIG", "default")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
