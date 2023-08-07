import json
import logging
import os
import pathlib
import shutil
from multiprocessing import Process, Manager

from minio import Minio
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.python import without_none_values

from celery_broker.main import celery_app
from crawler.spiders.menesr import MenesrSpider
from database.mongo_adapter import mongo
from models.crawl import CrawlProcess
from models.enums import MetadataType, ProcessStatus
from services.accessibility_best_practices_calculator import LighthouseWrapper, AccessibilityError
from services.carbon_calculator import CarbonCalculator, CarbonCalculatorError
from services.responsiveness_calculator import ResponsivenessCalculator

logger = logging.getLogger(__name__)


def crawl(crawl_process: CrawlProcess, results: dict):
    crawler_settings = get_project_settings()
    custom_settings = without_none_values(
        {
            "DEPTH_LIMIT": crawl_process.config.parameters.depth,
            "CLOSESPIDER_PAGECOUNT": crawl_process.config.parameters.limit,
            "CUSTOM_HEADERS": crawl_process.config.headers or {},
        }
    )
    crawler_settings.update(custom_settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(MenesrSpider, crawl_process=crawl_process)
    process.start()
    results["base_file_path"] = crawl_process.base_file_path
    logger.info(crawl_process.metadata)
    results["metadata"] = dict(crawl_process.metadata.items())


@celery_app.task(name="crawl")
def start_crawl_process(crawl_process: CrawlProcess):
    crawl_process.status = ProcessStatus.STARTED
    mongo.update_crawl(crawl_process)
    with Manager() as manager:
        shared_dict = manager.dict()
        p = Process(target=crawl, kwargs={"crawl_process": crawl_process, "results": shared_dict})
        p.start()
        p.join()
        crawl_process.base_file_path = shared_dict["base_file_path"]
        for meta, meta_process in shared_dict["metadata"].items():
            crawl_process.metadata[meta] = meta_process
    crawl_process.status = ProcessStatus.SUCCESS
    mongo.update_crawl(crawl_process)
    return crawl_process


@celery_app.task(name="get_accessibility")
def get_accessibility(crawl_process: CrawlProcess):
    crawl_process.metadata.get(MetadataType.ACCESSIBILITY).status = ProcessStatus.STARTED
    mongo.update_metadata(crawl_process, MetadataType.ACCESSIBILITY)
    accessibility_calc = LighthouseWrapper()
    result = {}
    if accessibility_process := crawl_process.metadata.get(MetadataType.ACCESSIBILITY):
        for url in accessibility_process.urls:
            try:
                accessibility = accessibility_calc.get_accessibility(url)
            except AccessibilityError as e:
                crawl_process.metadata.get(MetadataType.ACCESSIBILITY).status = ProcessStatus.PARTIAL_ERROR
                mongo.update_metadata(crawl_process, MetadataType.ACCESSIBILITY)
                continue
            result[url] = accessibility
        if not result:
            crawl_process.metadata.get(MetadataType.ACCESSIBILITY).status = ProcessStatus.ERROR
        store_metadata_result(crawl_process, result, MetadataType.ACCESSIBILITY)
    if crawl_process.metadata.get(MetadataType.ACCESSIBILITY).status == ProcessStatus.STARTED:
        crawl_process.metadata.get(MetadataType.ACCESSIBILITY).status = ProcessStatus.SUCCESS
    mongo.update_metadata(crawl_process, MetadataType.ACCESSIBILITY)
    return result


@celery_app.task(name="get_technologies")
def get_technologies(crawl_process: CrawlProcess):
    if technologies_process := crawl_process.metadata.get(MetadataType.TECHNOLOGIES):
        logger.info(technologies_process.urls)
    # TODO implement this task


@celery_app.task(name="get_good_practices")
def get_good_practices(crawl_process: CrawlProcess):
    crawl_process.metadata.get(MetadataType.GOOD_PRACTICES).status = ProcessStatus.STARTED
    mongo.update_metadata(crawl_process, MetadataType.GOOD_PRACTICES)
    best_practices_calc = LighthouseWrapper()
    result = {}
    if best_practices_process := crawl_process.metadata.get(MetadataType.GOOD_PRACTICES):
        for url in best_practices_process.urls:
            try:
                best_practices = best_practices_calc.get_best_practices(url)
            except AccessibilityError as e:
                crawl_process.metadata.get(MetadataType.GOOD_PRACTICES).status = ProcessStatus.PARTIAL_ERROR
                mongo.update_metadata(crawl_process, MetadataType.GOOD_PRACTICES)
                continue
            result[url] = best_practices
        if not result:
            crawl_process.metadata.get(MetadataType.GOOD_PRACTICES).status = ProcessStatus.ERROR
        store_metadata_result(crawl_process, result, MetadataType.GOOD_PRACTICES)
    if crawl_process.metadata.get(MetadataType.GOOD_PRACTICES).status == ProcessStatus.STARTED:
        crawl_process.metadata.get(MetadataType.GOOD_PRACTICES).status = ProcessStatus.SUCCESS
    mongo.update_metadata(crawl_process, MetadataType.GOOD_PRACTICES)
    return result


@celery_app.task(name="get_responsiveness")
def get_responsiveness(crawl_process: CrawlProcess):
    crawl_process.metadata.get(MetadataType.RESPONSIVENESS).status = ProcessStatus.STARTED
    mongo.update_metadata(crawl_process, MetadataType.RESPONSIVENESS)
    responsive_calc = ResponsivenessCalculator()
    result = {}
    if carbon_footprint_process := crawl_process.metadata.get(MetadataType.RESPONSIVENESS):
        for url in carbon_footprint_process.urls:
            try:
                responsiveness = responsive_calc.get_responsiveness(url)
            except CarbonCalculatorError as e:
                crawl_process.metadata.get(MetadataType.RESPONSIVENESS).status = ProcessStatus.PARTIAL_ERROR
                mongo.update_metadata(crawl_process, MetadataType.RESPONSIVENESS)
                continue
            result[url] = responsiveness
        if not result:
            crawl_process.metadata.get(MetadataType.RESPONSIVENESS).status = ProcessStatus.ERROR
        store_metadata_result(crawl_process, result, MetadataType.RESPONSIVENESS)
    if crawl_process.metadata.get(MetadataType.RESPONSIVENESS).status == ProcessStatus.STARTED:
        crawl_process.metadata.get(MetadataType.RESPONSIVENESS).status = ProcessStatus.SUCCESS
    mongo.update_metadata(crawl_process, MetadataType.RESPONSIVENESS)
    return result


@celery_app.task(name="get_carbon_footprint")
def get_carbon_footprint(crawl_process: CrawlProcess):
    crawl_process.metadata.get(MetadataType.CARBON_FOOTPRINT).status = ProcessStatus.STARTED
    mongo.update_metadata(crawl_process, MetadataType.CARBON_FOOTPRINT)
    carbon_calc = CarbonCalculator()
    result = {}
    if carbon_footprint_process := crawl_process.metadata.get(MetadataType.CARBON_FOOTPRINT):
        for url in carbon_footprint_process.urls:
            try:
                carbon_footprint = carbon_calc.get_carbon_footprint(url)
            except CarbonCalculatorError as e:
                crawl_process.metadata.get(MetadataType.CARBON_FOOTPRINT).status = ProcessStatus.PARTIAL_ERROR
                mongo.update_metadata(crawl_process, MetadataType.CARBON_FOOTPRINT)
                continue
            result[url] = carbon_footprint
        if not result:
            crawl_process.metadata.get(MetadataType.CARBON_FOOTPRINT).status = ProcessStatus.ERROR
        store_metadata_result(crawl_process, result, MetadataType.CARBON_FOOTPRINT)
    if crawl_process.metadata.get(MetadataType.CARBON_FOOTPRINT).status == ProcessStatus.STARTED:
        crawl_process.metadata.get(MetadataType.CARBON_FOOTPRINT).status = ProcessStatus.SUCCESS
    mongo.update_metadata(crawl_process, MetadataType.CARBON_FOOTPRINT)
    return result


def store_metadata_result(crawl_process: CrawlProcess, result: dict, metadata_type: MetadataType):
    # TODO en attente du retour client pour l'arborescence
    file_path = pathlib.Path(
        f"{crawl_process.base_file_path}/{os.environ['METADATA_FOLDER_NAME']}/{metadata_type}.json"
    )
    file_path.parent.mkdir(exist_ok=True, parents=True)
    file_path.write_text(json.dumps(result, indent=4))


@celery_app.task(name="upload_html")
def upload_html(crawl_process: CrawlProcess):
    client = Minio(
        os.environ["STORAGE_SERVICE_URL"],
        access_key=open(os.environ["STORAGE_SERVICE_USERNAME_FILE"]).readline(),
        secret_key=open(os.environ["STORAGE_SERVICE_PASSWORD_FILE"]).readline(),
        secure=False,
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
    mongo.update_crawl(crawl_process)


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
