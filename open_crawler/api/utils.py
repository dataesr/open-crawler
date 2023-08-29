from fastapi import FastAPI

from api import router, testing_router


def create_api_app() -> FastAPI:
    api_app = FastAPI(
        title="Asynchronous tasks processing with Celery and RabbitMQ",
        description="Sample FastAPI Application to demonstrate Event " "driven architecture with Celery and RabbitMQ",
        version="1.0.0",
    )

    api_app.include_router(router.websites_router)
    api_app.include_router(testing_router.test_router)  # TODO only useful for testing purposes, should be commented
    return api_app
