import os

from kombu import Queue, Exchange


class BaseConfig:
    """Base configuration."""
    LOGGER_LEVEL = "INFO"
    LOGGER_FORMAT = "[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s"

    DEFAULT_RECRAWL_INTERVAL = os.getenv("DEFAULT_RECRAWL_INTERVAL", 30)

    MODE = os.getenv("MODE", "production")

    # GOOGLE_API_KEY
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Volume
    LOCAL_FILES_PATH = os.getenv("LOCAL_FILES_PATH", "/mounted/local_files/")

    # Storage
    STORAGE_SERVICE_USERNAME = os.getenv("STORAGE_SERVICE_USERNAME")
    STORAGE_SERVICE_PASSWORD = os.getenv("STORAGE_SERVICE_PASSWORD")
    STORAGE_SERVICE_URL = os.getenv("STORAGE_SERVICE_URL")
    STORAGE_SERVICE_REGION = os.getenv("STORAGE_SERVICE_REGION", default=None)
    STORAGE_SERVICE_SECURE = os.getenv(
        "STORAGE_SERVICE_SECURE", default='False').lower() in ('true', '1', 't')
    STORAGE_SERVICE_BUCKET_NAME = os.getenv("STORAGE_SERVICE_BUCKET_NAME")
    HTML_FOLDER_NAME = os.getenv("HTML_FOLDER_NAME", default="html")
    METADATA_FOLDER_NAME = os.getenv(
        "METADATA_FOLDER_NAME", default="metadata")

    # Mongo
    MONGO_URI = os.getenv("MONGO_URI", default="mongodb://mongodb:27017")
    MONGO_DBNAME = os.getenv("MONGO_DBNAME", default="open-crawler")
    MONGO_WEBSITES_COLLECTION = os.getenv(
        "MONGO_WEBSITES_COLLECTION", default="websites")
    MONGO_CRAWLS_COLLECTION = os.getenv(
        "MONGO_CRAWLS_COLLECTION", default="crawls")

    # Celery
    broker_url = os.getenv("CELERY_BROKER_URL", default="redis://redis:6379")
    result_backend = os.getenv(
        "CELERY_RESULT_BACKEND", default="redis://redis:6379")
    broker_heartbeat = os.getenv("CELERY_BROKER_HEARTBEAT", default=2)

    CRAWL_QUEUE_NAME = "crawl_queue"
    LIGHTHOUSE_QUEUE_NAME = "lighthouse_queue"
    TECHNOLOGIES_QUEUE_NAME = "technologies_queue"
    CARBON_QUEUE_NAME = "carbon_footprint_queue"
    FINALIZE_CRAWL_QUEUE_NAME = "finalize_crawl_queue"

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
            CARBON_QUEUE_NAME,
            Exchange(CARBON_QUEUE_NAME),
            routing_key=CARBON_QUEUE_NAME,
        ),
        Queue(
            FINALIZE_CRAWL_QUEUE_NAME,
            Exchange(FINALIZE_CRAWL_QUEUE_NAME),
            routing_key=FINALIZE_CRAWL_QUEUE_NAME,
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
        "get_carbon_footprint": {
            "queue": CARBON_QUEUE_NAME,
            "routing_key": CARBON_QUEUE_NAME,
        },
        "finalize_crawl": {
            "queue": FINALIZE_CRAWL_QUEUE_NAME,
            "routing_key": FINALIZE_CRAWL_QUEUE_NAME,
        },
    }

    def get(self, attribute_name: str):
        return self.__getattribute__(attribute_name)


class DevelopmentConfig(BaseConfig):
    pass


def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "default": BaseConfig
    }
    config_name = os.environ.get("CONFIG_PROFILE", "default")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
