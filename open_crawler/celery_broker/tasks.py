import logging
from multiprocessing import Process

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.python import without_none_values

from celery_broker.main import celery_app
from open_crawler.crawler.spiders.menesr import MenesrSpider

logger = logging.getLogger(__name__)


def crawl(url: str, depth: int, limit: int, headers: dict):
    crawler_settings = get_project_settings()
    custom_settings = without_none_values(
        {"DEPTH_LIMIT": depth, "CLOSESPIDER_PAGECOUNT": limit, "CUSTOM_HEADERS": headers or {}}
    )
    crawler_settings.update(custom_settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(MenesrSpider, url=url)
    process.start()


@celery_app.task()
def start_crawl_process(url: str, depth: int, limit: int, headers: dict):
    p = Process(target=crawl, kwargs={"url": url, "depth": depth, "limit": limit, "headers": headers})
    p.start()
    p.join()
