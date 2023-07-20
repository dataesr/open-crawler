from celery import chain
from fastapi import APIRouter
from pydantic import BaseModel

from celery_broker.tasks import start_crawl_process, upload_html

crawl_router = APIRouter(prefix="/crawl", tags=["crawler"], responses={404: {"description": "Not found"}})


class CrawlRequest(BaseModel):
    url: str
    depth: int = None
    limit: int = None
    headers: dict = None
    metadata: dict = None


@crawl_router.post("")
async def create_task(crawl_request: CrawlRequest):
    task = chain(
        start_crawl_process.s(crawl_request.url, crawl_request.depth, crawl_request.limit, crawl_request.headers),
        upload_html.si(crawl_request.url),
    ).apply_async()
    return {"task_id": task.id}
