# Standard library imports
import json
import os
import pathlib
import shutil
from multiprocessing import Process, Manager

# Third-party imports
from minio import Minio
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.python import without_none_values

# Local imports
import repositories
from celery_broker.main import celery_app
from crawler.spiders.menesr import MenesrSpider
from models.crawl import CrawlModel
from models.enums import MetadataType, ProcessStatus
from models.metadata import MetadataTask
from models.process import CrawlProcess
from services.accessibility_best_practices_calculator import (
    LighthouseWrapper,
    AccessibilityError,
    BestPracticesError,
)
from services.carbon_calculator import CarbonCalculator, CarbonCalculatorError
from services.crawler_logger import logger, set_file
from services.responsiveness_calculator import (
    ResponsivenessCalculator,
    ResponsivenessCalculatorError,
)
from services.technologies_calculator import (
    TechnologiesCalculator,
    TechnologiesError,
)


def update_crawl_status(crawl: CrawlModel, status: ProcessStatus):
    crawl.update_status(status=status)
    repositories.crawls.update(crawl)


def init_crawler_settings(crawl_process: CrawlProcess):
    settings = get_project_settings()
    custom_settings = without_none_values(
        {
            "DEPTH_LIMIT": crawl_process.config.parameters.depth,
            "CLOSESPIDER_PAGECOUNT": crawl_process.config.parameters.limit,
            "CUSTOM_HEADERS": crawl_process.config.headers or {},
        }
    )
    settings.update(custom_settings)
    return settings


def start_crawler_process(crawl_process: CrawlProcess, results: dict):
    process = CrawlerProcess(settings=init_crawler_settings(crawl_process))
    process.crawl(MenesrSpider, crawl_process=crawl_process)
    process.start()
    results["metadata"] = dict(crawl_process.metadata.items())


@celery_app.task(bind=True, name="crawl")
def start_crawl_process(self, crawl: CrawlModel) -> CrawlProcess:
    repositories.crawls.update_status(
        crawl_id=crawl.id, status=ProcessStatus.STARTED
    )
    set_file(crawl.id)
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


def handle_metadata_result(
    task: MetadataTask,
    crawl_process: CrawlProcess,
    result: dict,
    metadata_type: MetadataType,
):
    if not result:
        task.update(status=ProcessStatus.ERROR)
        repositories.crawls.update_task(
            crawl_id=crawl_process.id,
            task_name=metadata_type,
            task=task,
        )
        set_file(crawl_process.id)
        logger.error(f"{metadata_type} failed.")
        return
    store_metadata_result(crawl_process, result, metadata_type)
    if task.status == ProcessStatus.STARTED:
        task.update(status=ProcessStatus.SUCCESS)
        repositories.crawls.update_task(
            crawl_id=crawl_process.id,
            task_name=metadata_type,
            task=task,
        )
        logger.debug(f"{metadata_type} ended!")
    return result


def store_metadata_result(
    crawl_process: CrawlProcess, result: dict, metadata_type: MetadataType
):
    base_file_path = f"{os.environ['LOCAL_FILES_PATH']}/{crawl_process.id}"
    file_path = pathlib.Path(
        f"{base_file_path}/{os.environ['METADATA_FOLDER_NAME']}/{metadata_type}.json"
    )
    file_path.parent.mkdir(exist_ok=True, parents=True)
    file_path.write_text(json.dumps(result, indent=4))


def metadata_task(
    task: MetadataTask,
    crawl_process: CrawlProcess,
    metadata_type: MetadataType,
    calculator,
    method_name: str,
):
    calc_method = getattr(calculator, method_name)
    result = {}
    task.update(status=ProcessStatus.STARTED)
    set_file(crawl_process.id)
    logger.debug(f"{metadata_type} started!")
    repositories.crawls.update_task(
        crawl_id=crawl_process.id,
        task_name=metadata_type,
        task=task,
    )
    if metadata_process := crawl_process.metadata.get(metadata_type):
        for url in metadata_process.urls:
            try:
                data = calc_method(url)
                result[url] = data
            except (
                AccessibilityError,
                BestPracticesError,
                TechnologiesError,
                ResponsivenessCalculatorError,
                CarbonCalculatorError,
            ) as e:
                logger.warning(
                    f"An error occured for url {url} during {metadata_type} process. {e}"
                )
                if task.status != ProcessStatus.PARTIAL_ERROR:
                    task.update(status=ProcessStatus.PARTIAL_ERROR)
                    repositories.crawls.update_task(
                        crawl_id=crawl_process.id,
                        task_name=metadata_type,
                        task=task,
                    )
                continue
            except Exception as e:
                logger.error(
                    f"An unknown error occured for url {url} during {metadata_type} process. {e}"
                )
                if task.status != ProcessStatus.PARTIAL_ERROR:
                    task.update(status=ProcessStatus.PARTIAL_ERROR)
                    repositories.crawls.update_task(
                        crawl_id=crawl_process.id,
                        task_name=metadata_type,
                        task=task,
                    )
                continue
    return handle_metadata_result(task, crawl_process, result, metadata_type)


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
    set_file(crawl.id)
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
        f"{os.environ['LOCAL_FILES_PATH']}/{crawl.id}"
    )
    local_files_folder = os.environ["LOCAL_FILES_PATH"]

    prefix = crawl.config.url.replace("https://", "").replace("http://", "")

    for file in crawl_files_path.rglob("*.[hj][ts][mo][ln]"):
        file_path = str(file)
        client.fput_object(
            bucket_name=bucket_name,
            object_name=f"{prefix}{file_path.removeprefix(local_files_folder)}",
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


def assume_content_type(file_path: str) -> str:
    # sourcery skip: assign-if-exp, reintroduce-else
    if file_path.endswith("html"):
        return "text/html"
    if file_path.endswith("json"):
        return "application/json"
    return ""


METADATA_TASK_REGISTRY = {
    MetadataType.ACCESSIBILITY: get_accessibility,
    MetadataType.TECHNOLOGIES: get_technologies,
    MetadataType.GOOD_PRACTICES: get_good_practices,
    MetadataType.RESPONSIVENESS: get_responsiveness,
    MetadataType.CARBON_FOOTPRINT: get_carbon_footprint,
}
