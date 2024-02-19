from celery import Celery
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.extentions import celery_app, api_app
from app.config import settings
from app.api import crawls_router, websites_router


def create_api_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    # Configure CORS for non-production modes
    deployment_mode = settings.MODE
    if deployment_mode != "production":
        api_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    api_app.include_router(websites_router)
    api_app.include_router(crawls_router)
    return api_app


def create_celery_app() -> Celery:
    celery_app.config_from_object(settings, namespace="CELERY")

    celery_config_updates = {
        "broker": settings.broker_url,
        "result_backend": settings.result_backend,
        "broker_connection_retry_on_startup": True,
        "broker_connection_max_retries": 10,
        "include": ["app.tasks"],
        "task_track_started": True,
        "task_serializer": "pickle",
        "result_serializer": "pickle",
        "accept_content": ["pickle", "json"],
        "result_persistent": True,
        "worker_send_task_events": True,
        "worker_prefetch_multiplier": 1,
    }
    celery_app.conf.update(celery_config_updates)
    celery_app.finalize()

    return celery_app
