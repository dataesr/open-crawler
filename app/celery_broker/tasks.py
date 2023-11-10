# Standard library imports
import os
import pathlib
import shutil
from multiprocessing import Process, Manager

# Third-party imports
from minio import Minio

# Local imports
import app.repositories as repositories
from app.celery_broker.crawler_utils import start_crawler_process
from app.celery_broker.main import celery_app
from app.celery_broker.metadata_utils import metadata_task
from app.celery_broker.utils import assume_content_type
from app.models.crawl import CrawlModel
from app.models.enums import MetadataType, ProcessStatus
from app.models.metadata import MetadataTask
from app.models.process import CrawlProcess
from app.services.accessibility_best_practices_calculator import (
    LighthouseWrapper,
)
from app.services.carbon_calculator import CarbonCalculator
from app.services.crawler_logger import logger
from app.services.responsiveness_calculator import (
    ResponsivenessCalculator,
)
from app.services.technologies_calculator import (
    TechnologiesCalculator,
)


@celery_app.task(bind=True, name="crawl")
def start_crawl_process(self, crawl: CrawlModel) -> CrawlProcess:
    repositories.crawls.update_status(
        crawl_id=crawl.id, status=ProcessStatus.STARTED
    )
    logger.debug("Html crawl started!")
    crawl.html_crawl.update(
        task_id=self.request.id, status=ProcessStatus.STARTED
    )
    repositories.crawls.update_task(
        crawl_id=crawl.id,
        task_name="html_crawl",
        task=crawl.html_crawl,
    )

    crawl_process = CrawlProcess.from_model(crawl)
    with Manager() as manager:
        shared_dict = manager.dict()
        p = Process(
            target=start_crawler_process,
            kwargs={"crawl_process": crawl_process, "results": shared_dict},
        )
        p.start()
        p.join()  # TODO define and add a timeout
        crawl_process.metadata.update(shared_dict["metadata"])

    crawl.html_crawl.update(status=ProcessStatus.SUCCESS)
    repositories.crawls.update_task(
        crawl_id=crawl.id,
        task_name="html_crawl",
        task=crawl.html_crawl,
    )
    logger.debug("Html crawl ended!")
    return crawl_process


@celery_app.task(bind=True, name="get_accessibility")
def get_accessibility(self, crawl_process: CrawlProcess):
    return metadata_task(
        task=MetadataTask(task_id=self.request.id),
        crawl_process=crawl_process,
        metadata_type=MetadataType.ACCESSIBILITY,
        calculator=LighthouseWrapper(),
        method_name="get_accessibility",
    )


@celery_app.task(bind=True, name="get_technologies")
def get_technologies(self, crawl_process: CrawlProcess):
    return metadata_task(
        task=MetadataTask(task_id=self.request.id),
        crawl_process=crawl_process,
        metadata_type=MetadataType.TECHNOLOGIES,
        calculator=TechnologiesCalculator(),
        method_name="get_technologies",
    )


@celery_app.task(bind=True, name="get_good_practices")
def get_good_practices(self, crawl_process: CrawlProcess):
    return metadata_task(
        task=MetadataTask(task_id=self.request.id),
        crawl_process=crawl_process,
        metadata_type=MetadataType.GOOD_PRACTICES,
        calculator=LighthouseWrapper(),
        method_name="get_best_practices",
    )


@celery_app.task(bind=True, name="get_responsiveness")
def get_responsiveness(self, crawl_process: CrawlProcess):
    return metadata_task(
        task=MetadataTask(task_id=self.request.id),
        crawl_process=crawl_process,
        metadata_type=MetadataType.RESPONSIVENESS,
        calculator=ResponsivenessCalculator(),
        method_name="get_responsiveness",
    )


@celery_app.task(bind=True, name="get_carbon_footprint")
def get_carbon_footprint(self, crawl_process: CrawlProcess):
    return metadata_task(
        task=MetadataTask(task_id=self.request.id),
        crawl_process=crawl_process,
        metadata_type=MetadataType.CARBON_FOOTPRINT,
        calculator=CarbonCalculator(),
        method_name="get_carbon_footprint",
    )


@celery_app.task(bind=True, name="upload_html")
def upload_html(self, crawl: CrawlModel):
    crawl.uploads.update(task_id=self.request.id, status=ProcessStatus.STARTED)
    logger.debug("Files upload started!")
    repositories.crawls.update_task(
        crawl_id=crawl.id,
        task_name="uploads",
        task=crawl.uploads,
    )

    client = Minio(
        endpoint=os.environ["STORAGE_SERVICE_URL"],
        access_key=os.environ["STORAGE_SERVICE_USERNAME"],
        secret_key=os.environ["STORAGE_SERVICE_PASSWORD"],
        secure=os.environ.get("STORAGE_SERVICE_SECURE", False),
        region=os.environ.get("STORAGE_SERVICE_REGION", None),
    )

    bucket_name = os.environ["STORAGE_SERVICE_BUCKET_NAME"]

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    crawl_files_path = pathlib.Path(
        f"/{os.environ['LOCAL_FILES_PATH'].strip('/')}/{crawl.id}"
    )
    local_files_folder = f"/{os.environ['LOCAL_FILES_PATH'].strip('/')}"

    prefix = crawl.config.url.replace("https://", "").replace("http://", "")

    for file in crawl_files_path.rglob("*.[hj][ts][mo][ln]"):
        file_path = str(file)
        client.fput_object(
            bucket_name=bucket_name,
            object_name=f"{file_path.removeprefix(local_files_folder).lstrip('/')}",
            file_path=file_path,
            content_type=assume_content_type(file_path),
        )
        os.remove(file)
    shutil.rmtree(crawl_files_path, ignore_errors=True)
    crawl.uploads.update(status=ProcessStatus.SUCCESS)
    repositories.crawls.update_task(
        crawl_id=crawl.id,
        task_name="uploads",
        task=crawl.uploads,
    )
    logger.debug("Files upload ended!")
    repositories.crawls.update_status(
        crawl_id=crawl.id, status=ProcessStatus.SUCCESS
    )
    logger.info(
        f"Crawl process ({crawl.id}) for website {crawl.config.url} ended"
    )

    repositories.websites.store_last_crawl(
        website_id=crawl.website_id,
        crawl=repositories.crawls.get(crawl_id=crawl.id).model_dump(),
    )


METADATA_TASK_REGISTRY = {
    MetadataType.ACCESSIBILITY: get_accessibility,
    MetadataType.TECHNOLOGIES: get_technologies,
    MetadataType.GOOD_PRACTICES: get_good_practices,
    MetadataType.RESPONSIVENESS: get_responsiveness,
    MetadataType.CARBON_FOOTPRINT: get_carbon_footprint,
}
