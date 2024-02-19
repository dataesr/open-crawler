# Local imports
from app.repositories.crawls import crawls
from app.repositories.websites import websites
from app.extentions import celery_app
from app.models.enums import ProcessStatus
from app.services.logging import logger


@celery_app.task(bind=True, name="finalize_crawl")
def finalize_crawl_process(self, crawl_id: str):
    logger.info(f"Crawl process ({crawl_id}) ended")
    crawl = crawls.get(crawl_id=crawl_id)

    statusses = {
        "html_crawl": crawl.html_crawl.status if crawl.html_crawl.enabled == True else None,
        "lighthouse": crawl.lighthouse.status if crawl.lighthouse.enabled == True else None,
        "technologies_and_trackers": crawl.technologies_and_trackers.status if crawl.technologies_and_trackers.enabled == True else None,
        "carbon_footprint": crawl.carbon_footprint.status if crawl.carbon_footprint.enabled == True else None,
    }
    error_count = len(
        [task for task, status in statusses.items() if status == ProcessStatus.ERROR])
    enabled_count = len(
        [task for task, status in statusses.items() if status is not None])
    status = ProcessStatus.PARTIAL_ERROR
    if error_count == 0:
        status = ProcessStatus.SUCCESS
    if error_count == enabled_count:
        status = ProcessStatus.ERROR

    crawls.update_status(
        crawl_id=crawl.id, status=status)

    websites.store_last_crawl(
        website_id=crawl.website_id,
        crawl=crawls.get(crawl_id=crawl.id).model_dump(),
    )
    return
