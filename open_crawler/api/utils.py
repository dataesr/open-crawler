from fastapi import FastAPI

from open_crawler.api import router


def create_api_app() -> FastAPI:
    api_app = FastAPI(
        title="Asynchronous tasks processing with Celery and RabbitMQ",
        description="Sample FastAPI Application to demonstrate Event " "driven architecture with Celery and RabbitMQ",
        version="1.0.0",
    )

    api_app.include_router(router.crawl_router)
    return api_app
