import logging

from celery import chain
from fastapi import APIRouter

from models.request import CrawlRequest
from celery_broker.tasks import start_crawl_process, upload_html
from database.mongo_adapter import mongo
from models.crawl import CrawlProcess

crawl_router = APIRouter(prefix="/crawl", tags=["crawler"], responses={404: {"description": "Not found"}})

logger = logging.getLogger(__name__)


@crawl_router.post("")
async def create_task(crawl_request: CrawlRequest):
    crawl: CrawlProcess = CrawlProcess(config=crawl_request.to_config())
    mongo.new_crawl(crawl)
    task = chain(
        start_crawl_process.s(crawl),
        upload_html.s(),
    ).apply_async()

    return {"task_id": task.id}
