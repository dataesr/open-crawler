import logging

from celery.result import AsyncResult
from fastapi import APIRouter

test_router = APIRouter(prefix="/test", tags=["test"], responses={404: {"description": "Not found"}})

logger = logging.getLogger(__name__)

@test_router.get("/task/{task_id}/status")
async def get_task_status(task_id: str):
    return {"status": AsyncResult(task_id).state}

