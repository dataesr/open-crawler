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


@retry(Exception, tries=1)
def run_lighthouse(url: str) -> Any:
    if not url:
        raise ValueError("URL cannot be empty.")
    lighthouse_process = subprocess.run(
        " ".join(
            [
                "lighthouse",
                url,
                '--chrome-flags="--no-sandbox --headless --disable-dev-shm-usage"',
                "--output=json",
                "--disable-full-page-screenshot",
                "--no-enable-error-reporting",
                "--quiet",
            ]
        ),
        stdout=subprocess.PIPE,
        shell=True,
    )
    return json.loads(lighthouse_process.stdout)


@celery_app.task(bind=True, name="get_lighthouse")
def get_lighthouse(self, crawl_id: str):
    crawl = crawls.get(crawl_id=crawl_id)
    meta = crawl.lighthouse
    meta.update(status=ProcessStatus.STARTED, task_id=self.request.id)
    crawls.update_task(crawl_id=crawl.id,
                       task_name="lighthouse", task=meta)
    result = None
    try:
        result = run_lighthouse(url=crawl.url)
    except Exception as e:
        logger.error(
            f"An error occurred for url {crawl.url} during lighthouse process: {e}")
        meta.update(status=ProcessStatus.ERROR)
    if not result:
        logger.error(f"No lighthouse result for url {crawl.url}")
        meta.update(status=ProcessStatus.ERROR)
    try:
        if result:
            files.store_metadata_file(
                crawl_id=crawl_id,
                key="lighthouse.json",
                data=json.dumps(result, indent=2, default=str)
            )
    except Exception as e:
        logger.error(
            f"Error occured while uploding lighthouse result for url {crawl.url}: {e}")
        meta.update(status=ProcessStatus.ERROR)
    if meta.status != ProcessStatus.ERROR:
        meta.update(status=ProcessStatus.SUCCESS)
    crawls.update_task(crawl_id=crawl.id,
                       task_name="lighthouse", task=meta)
    return
