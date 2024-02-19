from celery import group, chain, chord
from app.models.enums import MetadataType

from app.tasks import (
    get_lighthouse,
    get_technologies,
    get_carbon_footprint,
    get_html_crawl,
    finalize_crawl_process,
)

from app.models.crawl import CrawlModel
from app.services.logging import logger

METADATA_TASK_REGISTRY = {
    MetadataType.LIGHTHOUSE: get_lighthouse,
    MetadataType.TECHNOLOGIES: get_technologies,
    MetadataType.CARBON_FOOTPRINT: get_carbon_footprint,
}


def start_crawl(crawl: CrawlModel) -> None:
    logger.info(f"New crawl process ({crawl.id}) for website {crawl.url}")
    logger.info(
        f"New crawl process ({crawl.id}) for website {crawl.url}"
    )
    metadata_tasks = group(
        METADATA_TASK_REGISTRY.get(metadata).si(crawl.id)
        for metadata in crawl.enabled_metadata
    )
    # If a task in a chain fails, the remaining tasks in the chain will not be executed.
    # To ensure that `finalize_crawl` is executed regardless of whether the previous tasks in the chain fail or succeed,
    # We need to put it in the `link_error` callback in start_crawl_process and do a chord with the metadata tasks.
    chain(
        get_html_crawl.si(crawl.id).on_error(
            finalize_crawl_process.si(crawl.id)),
        chord(metadata_tasks, finalize_crawl_process.si(crawl.id)),
        finalize_crawl_process.si(crawl.id)
    ).apply_async(task_id=crawl.id)
