from urllib.parse import urlparse

from celery import group, chain

import app.repositories as repositories
from app.celery_broker.tasks import (
    METADATA_TASK_REGISTRY,
    start_crawl_process,
)
from app.models.crawl import CrawlModel
from app.models.enums import ProcessStatus
from app.models.website import WebsiteModel
from app.services.crawler_logger import logger


def create_crawl(website: WebsiteModel) -> CrawlModel:

    # Check if the path component of the URL is empty or "/"
    # If the crawl target is a single page, we will ignore the depth and the limit in the request.
    if not is_domain(website.url):
        website.depth = 0
        website.limit = 1
        logger.warning("The url to crawl is not a domain. Only one page will be crawled")

    crawl: CrawlModel = CrawlModel(
        website_id=website.id,
        config=website.to_config(),
    )
    crawl.init_tasks()
    repositories.crawls.create(crawl)
    return crawl


def start_crawl(crawl: CrawlModel) -> None:
    logger.info(
        f"New crawl process ({crawl.id}) for website {crawl.config.url}"
    )
    metadata_tasks = group(
        METADATA_TASK_REGISTRY.get(metadata).s()
        for metadata in crawl.enabled_metadata
    )
    chain(
        start_crawl_process.s(crawl),
        metadata_tasks,
    ).apply_async(task_id=crawl.id)


def is_domain(url: str) -> bool:
    parsed_url = urlparse(url)
    return parsed_url.path == '' or parsed_url.path == '/'

