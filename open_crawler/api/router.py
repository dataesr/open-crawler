from fastapi import APIRouter
from scrapy.utils.project import get_project_settings

from open_crawler.celery_broker.tasks import get_crawl_task

crawl_router = APIRouter(prefix='/crawl', tags=['crawler'], responses={404: {"description": "Not found"}})


@crawl_router.post("/demo")
async def demo(url: str):
    project_settings = get_project_settings()
    get_crawl_task.apply_async(args=[url])
    return {"message": "Crawling started"}




