from celery import group, chain

import app.repositories as repositories
from app.celery_broker.tasks import (
    METADATA_TASK_REGISTRY,
    start_crawl_process,
    upload_html,
)
from app.models.crawl import CrawlModel
from app.models.website import WebsiteModel
from app.services.crawler_logger import logger


def create_crawl(website: WebsiteModel) -> CrawlModel:
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
        upload_html.si(crawl),
    ).apply_async(task_id=crawl.id)
