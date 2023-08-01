import json
import logging
import os
import pathlib
import shutil
from multiprocessing import Process, Manager
from urllib.parse import urlparse

from minio import Minio
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.python import without_none_values

from celery_broker.main import celery_app
from crawler.spiders.menesr import MenesrSpider
from database.mongo_adapter import mongo
from models.crawl import CrawlProcess
from models.enums import MetadataType, ProcessStatus
from services.carbon_calculator import CarbonCalculator

logger = logging.getLogger(__name__)


# class CustomManager(BaseManager):
#     pass


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
    if accessibility_process := crawl_process.metadata.get(MetadataType.ACCESSIBILITY):
        logger.info(accessibility_process.urls)
    # TODO implement this task


@celery_app.task(name="get_technologies")
def get_technologies(crawl_process: CrawlProcess):
    if technologies_process := crawl_process.metadata.get(MetadataType.TECHNOLOGIES):
        logger.info(technologies_process.urls)
    # TODO implement this task


@celery_app.task(name="get_good_practices")
def get_good_practices(crawl_process: CrawlProcess):
    if good_practices_process := crawl_process.metadata.get(MetadataType.GOOD_PRACTICES):
        logger.info(good_practices_process.urls)
    # TODO implement this task


@celery_app.task(name="get_responsiveness")
def get_responsiveness(crawl_process: CrawlProcess):
    if responsiveness_process := crawl_process.metadata.get(MetadataType.RESPONSIVENESS):
        logger.info(responsiveness_process.urls)
    # TODO implement this task


@celery_app.task(name="get_carbon_footprint")
def get_carbon_footprint(crawl_process: CrawlProcess):
    crawl_process.metadata.get(MetadataType.CARBON_FOOTPRINT).status = ProcessStatus.STARTED
    mongo.update_metadata(crawl_process, MetadataType.CARBON_FOOTPRINT)
    carbon_calc = CarbonCalculator()
    result = {}
    if carbon_footprint_process := crawl_process.metadata.get(MetadataType.CARBON_FOOTPRINT):
        for url in carbon_footprint_process.urls:
            carbon_footprint = carbon_calc.get_carbon_footprint(url)
            result[url] = carbon_footprint
        file_path = pathlib.Path(f"{crawl_process.base_file_path}/metadata/{MetadataType.CARBON_FOOTPRINT}.json")
        file_path.parent.mkdir(exist_ok=True, parents=True)
        file_path.write_text(json.dumps(result, indent=4))
    crawl_process.metadata.get(MetadataType.CARBON_FOOTPRINT).status = ProcessStatus.SUCCESS
    mongo.update_metadata(crawl_process, MetadataType.CARBON_FOOTPRINT)
    return result


@celery_app.task(name="upload_html")
def upload_html(crawl_process: CrawlProcess):
    tmp_folder = "/tmp/"
    bucket_name = "tmp"

    client = Minio(
        "minio:9000",
        access_key=os.environ["MINIO_ROOT_USER"],
        secret_key=os.environ["MINIO_ROOT_PASSWORD"],
        secure=False,
    )

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    upload_root = pathlib.Path(f"{crawl_process.base_file_path}")

    for html_file in upload_root.rglob("*.html"):
        client.fput_object(
            bucket_name, str(html_file).replace(tmp_folder, "", 1), str(html_file), content_type="text/html"
        )
        os.remove(html_file)
    for json_file in upload_root.rglob("*.json"):
        client.fput_object(
            bucket_name, str(json_file).replace(tmp_folder, "", 1), str(json_file), content_type="application/json"
        )
        os.remove(json_file)
    shutil.rmtree(upload_root, ignore_errors=True)
    crawl_process.status = ProcessStatus.SUCCESS
    mongo.update_crawl(crawl_process)


METADATA_TASK_REGISTRY = {
    MetadataType.ACCESSIBILITY: get_accessibility,
    MetadataType.TECHNOLOGIES: get_technologies,
    MetadataType.GOOD_PRACTICES: get_good_practices,
    MetadataType.RESPONSIVENESS: get_responsiveness,
    MetadataType.CARBON_FOOTPRINT: get_carbon_footprint,
}
