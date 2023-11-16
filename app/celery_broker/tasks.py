# Standard library imports
import os
import pathlib
import shutil
from multiprocessing import Process, Manager

# Local imports
from app.repositories.crawls import crawls
from app.repositories.files import files
from app.celery_broker.crawler_utils import start_crawler_process, set_html_crawl_status
from app.celery_broker.main import celery_app
from app.celery_broker.metadata_utils import metadata_task
from app.celery_broker.utils import assume_content_type
from app.config import settings
from app.models.crawl import CrawlModel
from app.models.enums import MetadataType, ProcessStatus
from app.models.metadata import MetadataTask
from app.models.process import CrawlProcess
from app.services.lighthouse_calculator import (
    LighthouseCalculator,
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
    crawls.update_status(
        crawl_id=crawl.id, status=ProcessStatus.STARTED
    )
    logger.debug("Html crawl started!")
    set_html_crawl_status(crawl, self.request.id, ProcessStatus.STARTED)

    crawl_process = CrawlProcess.from_model(crawl)

    try:
        with Manager() as manager:
            shared_dict = manager.dict()
            p = Process(
                target=start_crawler_process,
                kwargs={"crawl_process": crawl_process, "results": shared_dict},
            )
            p.start()
            p.join()  # TODO define and add a timeout
            crawl_process.metadata.update(shared_dict["metadata"])
    except Exception as e:
        logger.error(f"Error while crawling html files: {e}")
        set_html_crawl_status(crawl, self.request.id, ProcessStatus.ERROR)
        self.update_state(state='FAILURE')
        return crawl_process
    try:
        # Attempt to upload HTML files associated with the crawl
        upload_html(crawl)
    except Exception as e:
        logger.error(f"Error while uploading html files: {e}")
        # Html crawl will be considered failed if we can't upload the html files
        set_html_crawl_status(crawl, self.request.id, ProcessStatus.ERROR)
        self.update_state(state='FAILURE')
        return crawl_process

    set_html_crawl_status(crawl, self.request.id, ProcessStatus.SUCCESS)

    logger.debug("Html crawl ended!")
    return crawl_process


@celery_app.task(bind=True, name="get_lighthouse")
def get_lighthouse(self, crawl_process: CrawlProcess):
    return metadata_task(
        task=MetadataTask(task_id=self.request.id),
        crawl_process=crawl_process,
        metadata_type=MetadataType.LIGHTHOUSE,
        calculator=LighthouseCalculator(),
        method_name="get_lighthouse",
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


METADATA_TASK_REGISTRY = {
    MetadataType.LIGHTHOUSE: get_lighthouse,
    MetadataType.TECHNOLOGIES: get_technologies,
    MetadataType.RESPONSIVENESS: get_responsiveness,
    MetadataType.CARBON_FOOTPRINT: get_carbon_footprint,
}


def upload_html(crawl: CrawlModel):
    crawl_files_path = pathlib.Path(
        f"/{settings.LOCAL_FILES_PATH.strip('/')}/{crawl.id}"
    )
    local_files_folder = f"/{settings.LOCAL_FILES_PATH.strip('/')}"

    for file in crawl_files_path.rglob("*.[hj][ts][mo][ln]"):
        file_path = str(file)
        file_name = file_path.removeprefix(local_files_folder).lstrip('/')
        files.store_html_file(
            object_name=file_name,
            file_path=file_path,
            content_type=assume_content_type(file_path),
        )
        os.remove(file)
    shutil.rmtree(crawl_files_path, ignore_errors=True)
