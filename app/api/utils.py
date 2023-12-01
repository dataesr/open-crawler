from urllib.parse import urlparse

from celery import group, chain, chord

from app.repositories.crawls import crawls
from app.celery_broker.tasks import (
    METADATA_TASK_REGISTRY,
    start_crawl_process, finalize_crawl_process,
)
from app.models.crawl import CrawlModel
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
    crawls.create(crawl)
    return crawl


def start_crawl(crawl: CrawlModel) -> None:
    logger.info(
        f"New crawl process ({crawl.id}) for website {crawl.config.url}"
    )
    metadata_tasks = group(
        METADATA_TASK_REGISTRY.get(metadata).s()
        for metadata in crawl.enabled_metadata
    )
    # If a task in a chain fails, the remaining tasks in the chain will not be executed.
    # To ensure that `finalize_crawl` is executed regardless of whether the previous tasks in the chain fail or succeed,
    # We need to put it in the `link_error` callback in start_crawl_process and do a chord with the metadata tasks.
    chain(
        start_crawl_process.s(crawl).on_error(finalize_crawl_process.s(crawl)),
        chord(metadata_tasks, finalize_crawl_process.s(crawl)),
    ).apply_async(task_id=crawl.id)


def is_domain(url: str) -> bool:
    parsed_url = urlparse(url)
    return parsed_url.path == '' or parsed_url.path == '/'

