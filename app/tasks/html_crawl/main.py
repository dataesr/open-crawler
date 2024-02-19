from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.python import without_none_values
from multiprocessing import Process

from app.repositories.crawls import crawls
from app.repositories.websites import websites
from app.extentions import celery_app
from app.models.enums import ProcessStatus
from app.services.logging import logger
from app.tasks.html_crawl.spider import MenesrSpider
from app.models.crawl import HTMLCrawlModel


def start_crawl(html_crawl: HTMLCrawlModel, url: str, crawl_id: str):
    settings = get_project_settings()
    custom_settings = without_none_values({
        "DEPTH_LIMIT": html_crawl.depth | 0,
        "CUSTOM_HEADERS": html_crawl.headers or {},
    })
    settings.update(custom_settings)
    process = CrawlerProcess(settings=settings)
    process.crawl(MenesrSpider, crawl_id=crawl_id, url=url, crawl=html_crawl)
    process.start()


@celery_app.task(bind=True, name="crawl")
def get_html_crawl(self, crawl_id):
    crawl = crawls.get(crawl_id=crawl_id)
    crawls.update_status(crawl_id=crawl.id, status=ProcessStatus.STARTED)
    websites.store_last_crawl(
        website_id=crawl.website_id,
        crawl=crawls.get(crawl_id=crawl.id).model_dump(),
    )
    html_crawl = crawl.html_crawl
    html_crawl.update(status=ProcessStatus.STARTED, task_id=self.request.id)
    crawls.update_task(crawl_id=crawl.id,
                       task_name="html_crawl", task=html_crawl)
    logger.debug("Html crawl started!")

    # We start the crawl in a separate process so each
    # crawl creates its own Twisted reactor
    process = Process(
        target=start_crawl,
        kwargs={"html_crawl": html_crawl, "url": crawl.url, "crawl_id": crawl.id})
    process.start()
    process.join(120)  # Wait 120 seconds for the crawler to finish
    if process.is_alive():
        logger.error(
            "Crawler timed out, the crawl may not contain enough pages")
        process.terminate()
        process.join()
    return
