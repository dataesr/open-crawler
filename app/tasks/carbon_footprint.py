import requests
import json
from retry import retry
from typing import Any
# Local imports
from app.extentions import celery_app
from app.models.enums import ProcessStatus
from app.repositories.crawls import crawls
from app.repositories.files import files
from app.services.logging import logger

TIMEOUT = 60  # 5 minutes timeout for the API request
BASE_URL = "https://api.websitecarbon.com/site"


@retry(Exception, tries=3, delay=2, backoff=2)
def run_carbon_footprint(url: str) -> dict[str, Any]:
    if not url:
        raise ValueError("URL cannot be empty.")
    try:
        response = requests.get(
            BASE_URL, params={"url": url}, timeout=TIMEOUT
        )
        response.raise_for_status()
        response_json = response.json()
    except requests.RequestException as e:
        raise Exception(
            f"Request to Carbon Calculator API failed: {str(e)}"
        ) from e
    except ValueError as e:
        # This will catch JSON decoding errors
        raise Exception(
            f"Failed to decode API response: {str(e)}"
        ) from e
    return response_json


@celery_app.task(bind=True, name="get_carbon_footprint")
def get_carbon_footprint(self, crawl_id: str):
    crawl = crawls.get(crawl_id=crawl_id)
    meta = crawl.carbon_footprint
    meta.update(status=ProcessStatus.STARTED, task_id=self.request.id)
    crawls.update_task(crawl_id=crawl.id,
                       task_name="carbon_footprint", task=meta)
    result = None
    try:
        result = run_carbon_footprint(url=crawl.url)
    except Exception as e:
        logger.error(
            f"An error occurred for url {crawl.url} during carbon_footprint process: {e}")
        meta.update(status=ProcessStatus.ERROR)
    if not result:
        logger.error(f"No carbon_footprint result for url {crawl.url}")
        meta.update(status=ProcessStatus.ERROR)
    try:
        if result:
            files.store_metadata_file(
                crawl_id=crawl_id,
                key="carbon_footprint.json",
                data=json.dumps(result, indent=2, default=str)
            )
    except Exception as e:
        logger.error(
            f"Error occured while uploding carbon_footprint result for url {crawl.url}: {e}")
        meta.update(status=ProcessStatus.ERROR)
    if meta.status != ProcessStatus.ERROR:
        meta.update(status=ProcessStatus.SUCCESS)
    crawls.update_task(crawl_id=crawl.id,
                       task_name="carbon_footprint", task=meta)
    return
