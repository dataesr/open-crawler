import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router, testing_router


def create_api_app() -> FastAPI:
    api_app = FastAPI(
        title="Asynchronous tasks processing with Celery and RabbitMQ",
        description="Sample FastAPI Application to demonstrate Event " "driven architecture with Celery and RabbitMQ",
        version="1.0.0",
    )

    mode = os.environ.get("MODE", "production")
    if mode != "production":
        api_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    api_app.include_router(router.websites_router)
    # TODO only useful for testing purposes, should be commented
    api_app.include_router(testing_router.test_router)
    return api_app
