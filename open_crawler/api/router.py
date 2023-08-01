import logging

from celery import chain, group
from fastapi import APIRouter

from celery_broker.tasks import start_crawl_process, upload_html, METADATA_TASK_REGISTRY
from database.mongo_adapter import mongo
from models.crawl import CrawlProcess
from models.request import CrawlRequest

crawl_router = APIRouter(prefix="/crawl", tags=["crawler"], responses={404: {"description": "Not found"}})

logger = logging.getLogger(__name__)


@crawl_router.post("")
async def create_task(crawl_request: CrawlRequest):
    crawl: CrawlProcess = CrawlProcess(config=crawl_request.to_config())
    mongo.new_crawl(crawl)
    metadata_tasks = group(METADATA_TASK_REGISTRY.get(metadata).s() for metadata in crawl.enabled_metadata)
    task = chain(
        start_crawl_process.s(crawl),
        metadata_tasks,
        upload_html.si(crawl),
    ).apply_async()

    return {"task_id": task.id}
