import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.crawls_router import crawls_router
from api.websites_router import websites_router


def create_api_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    api_app = FastAPI(
        title="Module de crawl pour le projet Scanr",
        description="Application permettant de crawler des sites web et d'en extraire certaines métadonnées.",
        version="1.0.0",
    )

    # Configure CORS for non-production modes
    deployment_mode = os.environ.get("MODE", "production")
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
