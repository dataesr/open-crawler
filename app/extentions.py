from celery import Celery
from fastapi import FastAPI

# Instanciate celery and finilaze it in factory
celery_app = Celery(__name__, autofinalize=False)

# Instanciate FastAPI and configure it in factory
api_app = FastAPI(
    title="Open Crawler API",
    description="Application permettant de crawler des sites web et d'en extraire certaines métadonnées.",
    version="1.0.0",
)
