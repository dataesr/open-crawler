from celery.result import AsyncResult
from fastapi import APIRouter
from pydantic import BaseModel

from open_crawler.celery_broker.tasks import start_crawl_process

crawl_router = APIRouter(prefix="/crawl", tags=["crawler"], responses={404: {"description": "Not found"}})


class CrawlRequest(BaseModel):
    url: str
    depth: int = None
    limit: int = None
    headers: dict = None
    metadata: dict = None


@crawl_router.post("")
async def create_task(crawl_request: CrawlRequest):
    task = start_crawl_process.delay(crawl_request.url, crawl_request.depth, crawl_request.limit, crawl_request.headers)
    return {"task_id": task.id}


@crawl_router.get("/task/{task_id}/status")
async def get_task_status(task_id: str):
    return {"status": AsyncResult(task_id).state}
