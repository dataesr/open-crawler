import logging
from multiprocessing import Process

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from celery_broker.main import celery_app
from open_crawler.crawler.spiders.menesr import MenesrSpider

logger = logging.getLogger(__name__)


def crawl(url: str, depth: int, limit: int, headers: dict):
    crawler_settings = get_project_settings()
    crawler_settings.set("DEPTH_LIMIT", depth)
    crawler_settings.set("CLOSESPIDER_PAGECOUNT", limit)
    crawler_settings.set("CUSTOM_HEADERS", headers or {})
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(MenesrSpider, url=url)
    process.start()


@celery_app.task()
def start_crawl_process(url: str, depth: int, limit: int, headers: dict):
    p = Process(target=crawl, kwargs={"url": url, "depth": depth, "limit": limit, "headers": headers})
    p.start()
    p.join()
