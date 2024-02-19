import json
import subprocess
from retry import retry
from typing import Any
# Local imports
from app.extentions import celery_app
from app.models.enums import ProcessStatus
from app.repositories.crawls import crawls
from app.repositories.files import files
from app.services.logging import logger


@retry(Exception, tries=3, delay=2, backoff=2)
def run_technologies(url: str) -> list[dict[str, Any]]:
    technologies_process = subprocess.run(
        " ".join(
            [
                "node",
                "/wappalyzer/src/drivers/npm/cli.js",
                url,
            ]
        ),
        stdout=subprocess.PIPE,
        shell=True,
    )
    technologies_response = json.loads(technologies_process.stdout)
    result = technologies_response["technologies"]
    # agnostic_result = [res for res in result if res["confidence"] == 100]
    return result


@celery_app.task(bind=True, name="get_technologies")
def get_technologies(self, crawl_id: str):
    crawl = crawls.get(crawl_id=crawl_id)
    meta = crawl.technologies_and_trackers
    meta.update(status=ProcessStatus.STARTED, task_id=self.request.id)
    crawls.update_task(crawl_id=crawl.id,
                       task_name="technologies_and_trackers", task=meta)
    result = None
    try:
        result = run_technologies(url=crawl.url)
    except Exception as e:
        logger.error(
            f"An error occurred for url {crawl.url} during technologies process: {e}")
        meta.update(status=ProcessStatus.ERROR)
    if not result:
        logger.error(f"No technologies result for url {crawl.url}")
        meta.update(status=ProcessStatus.ERROR)
    try:
        if result:
            files.store_metadata_file(
                crawl_id=crawl_id,
                key="technologies.json",
                data=json.dumps(result, indent=2, default=str)
            )
    except Exception as e:
        logger.error(
            f"Error occured while uploding technologies result for url {crawl.url}: {e}")
        meta.update(status=ProcessStatus.ERROR)
    if meta.status != ProcessStatus.ERROR:
        meta.update(status=ProcessStatus.SUCCESS)
    crawls.update_task(crawl_id=crawl.id,
                       task_name="technologies_and_trackers", task=meta)
    return
