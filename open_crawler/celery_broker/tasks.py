# Standard library imports
import json
import logging
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
from models.crawl import CrawlProcess
from models.enums import MetadataType, ProcessStatus

from crawler.spiders.menesr import MenesrSpider
from services.accessibility_best_practices_calculator import LighthouseWrapper, AccessibilityError, BestPracticesError
from services.carbon_calculator import CarbonCalculator, CarbonCalculatorError
from services.responsiveness_calculator import ResponsivenessCalculator, ResponsivenessCalculatorError
from services.technologies_calculator import TechnologiesCalculator, TechnologiesError

logger = logging.getLogger(__name__)


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
    results["base_file_path"] = crawl_process.base_file_path
    results["metadata"] = dict(crawl_process.metadata.items())


@celery_app.task(name="crawl")
def start_crawl_process(crawl_process: CrawlProcess):
    crawl_process.status = ProcessStatus.STARTED
    repositories.crawls.update_status(data=crawl_process)
    with Manager() as manager:
        shared_dict = manager.dict()
        p = Process(target=start_crawler_process, kwargs={
                    "crawl_process": crawl_process, "results": shared_dict})
        p.start()
        p.join()
        crawl_process.base_file_path = shared_dict["base_file_path"]
        crawl_process.metadata.update(shared_dict["metadata"])
    crawl_process.status = ProcessStatus.SUCCESS
    repositories.crawls.update_status(crawl_process)
    return crawl_process


def update_process_metadata(crawl_process: CrawlProcess, metadata_type: MetadataType, status: ProcessStatus):
    crawl_process.set_metadata_status(metadata_type, status)
    if crawl_process.metadata_needs_save(metadata_type):
        repositories.crawls.update_metadata(crawl_process, metadata_type)


def handle_metadata_result(crawl_process: CrawlProcess, result: dict, metadata_type: MetadataType):
    if not result:
        update_process_metadata(
            crawl_process, metadata_type, ProcessStatus.ERROR)
        return
    store_metadata_result(crawl_process, result, metadata_type)
    if crawl_process.metadata.get(metadata_type).status == ProcessStatus.STARTED:
        update_process_metadata(
            crawl_process, metadata_type, ProcessStatus.SUCCESS)
    return result


def store_metadata_result(crawl_process: CrawlProcess, result: dict, metadata_type: MetadataType):
    file_path = pathlib.Path(
        f"{crawl_process.base_file_path}/{os.environ['METADATA_FOLDER_NAME']}/{metadata_type}.json"
    )
    file_path.parent.mkdir(exist_ok=True, parents=True)
    file_path.write_text(json.dumps(result, indent=4))


def metadata_task(crawl_process: CrawlProcess, metadata_type: MetadataType, calculator, method_name: str):
    update_process_metadata(
        crawl_process, metadata_type, ProcessStatus.STARTED)
    calc_method = getattr(calculator, method_name)
    result = {}
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
            ):
                update_process_metadata(
                    crawl_process, metadata_type, ProcessStatus.PARTIAL_ERROR)
                continue
            except Exception:
                logger.error("Unknown error")
                update_process_metadata(
                    crawl_process, metadata_type, ProcessStatus.PARTIAL_ERROR)
                continue
    return handle_metadata_result(crawl_process, result, metadata_type)


@celery_app.task(name="get_accessibility")
def get_accessibility(crawl_process: CrawlProcess):
    return metadata_task(crawl_process, MetadataType.ACCESSIBILITY, LighthouseWrapper(), "get_accessibility")


@celery_app.task(name="get_technologies")
def get_technologies(crawl_process: CrawlProcess):
    return metadata_task(crawl_process, MetadataType.TECHNOLOGIES, TechnologiesCalculator(), "get_technologies")


@celery_app.task(name="get_good_practices")
def get_good_practices(crawl_process: CrawlProcess):
    return metadata_task(crawl_process, MetadataType.GOOD_PRACTICES, LighthouseWrapper(), "get_best_practices")


@celery_app.task(name="get_responsiveness")
def get_responsiveness(crawl_process: CrawlProcess):
    return metadata_task(crawl_process, MetadataType.RESPONSIVENESS, ResponsivenessCalculator(), "get_responsiveness")


@celery_app.task(name="get_carbon_footprint")
def get_carbon_footprint(crawl_process: CrawlProcess):
    return metadata_task(crawl_process, MetadataType.CARBON_FOOTPRINT, CarbonCalculator(), "get_carbon_footprint")


@celery_app.task(name="upload_html")
def upload_html(crawl_process: CrawlProcess):
    client = Minio(
        endpoint=os.environ["STORAGE_SERVICE_URL"],
        access_key=os.environ["STORAGE_SERVICE_USERNAME"],
        secret_key=os.environ["STORAGE_SERVICE_PASSWORD"],
        secure=os.environ["STORAGE_SERVICE_SECURE"] | False,
    )

    bucket_name = os.environ["STORAGE_SERVICE_BUCKET_NAME"]

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    crawl_files_path = pathlib.Path(crawl_process.base_file_path)
    local_files_folder = os.environ["LOCAL_FILES_PATH"]

    for file in crawl_files_path.rglob("*.[hj][ts][mo][ln]"):
        file_path = str(file)
        client.fput_object(
            bucket_name=bucket_name,
            object_name=file_path.removeprefix(local_files_folder),
            file_path=file_path,
            content_type=assume_content_type(file_path),
        )
        os.remove(file)
    shutil.rmtree(crawl_files_path, ignore_errors=True)
    crawl_process.status = ProcessStatus.SUCCESS
    repositories.crawls.update_status(crawl_process)


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
