from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.python import without_none_values

import app.repositories as repositories
from app.crawler.spider import MenesrSpider
from app.models.crawl import CrawlModel
from app.models.enums import ProcessStatus
from app.models.process import CrawlProcess


def update_crawl_status(crawl: CrawlModel, status: ProcessStatus):
    crawl.update_status(status=status)
    repositories.crawls.update(crawl)


def init_crawler_settings(crawl_process: CrawlProcess):
    settings = get_project_settings()
    custom_settings = without_none_values(
        {
            "DEPTH_LIMIT": crawl_process.config.parameters.depth,
            "CLOSESPIDER_PAGECOUNT": crawl_process.config.parameters.limit,
            "CUSTOM_HEADERS": crawl_process.config.headers or {},
        }
    )
    settings.update(custom_settings)
    return settings


def start_crawler_process(crawl_process: CrawlProcess, results: dict):
    process = CrawlerProcess(settings=init_crawler_settings(crawl_process))
    process.crawl(MenesrSpider, crawl_process=crawl_process)
    process.start()
    results["metadata"] = dict(crawl_process.metadata.items())
