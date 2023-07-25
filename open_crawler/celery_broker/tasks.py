import logging
import os
import pathlib
import shutil
from multiprocessing import Process
from urllib.parse import urlparse

from minio import Minio
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.python import without_none_values

from celery_broker.main import celery_app
from crawler.spiders.menesr import MenesrSpider
from database.mongo_adapter import mongo
from models.crawl import CrawlProcess
from models.enums import ProcessStatus

logger = logging.getLogger(__name__)


def crawl(crawl_process: CrawlProcess):
    crawler_settings = get_project_settings()
    custom_settings = without_none_values(
        {
            "DEPTH_LIMIT": crawl_process.config.parameters.depth,
            "CLOSESPIDER_PAGECOUNT": crawl_process.config.parameters.limit,
            "CUSTOM_HEADERS": crawl_process.config.headers or {}
        }
    )
    crawler_settings.update(custom_settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(MenesrSpider, url=crawl_process.config.url)
    process.start()


@celery_app.task(name="crawl")
def start_crawl_process(crawl_process: CrawlProcess):
    p = Process(target=crawl, kwargs={"crawl_process": crawl_process})
    p.start()
    p.join()
    crawl_process.status = ProcessStatus.STARTED
    mongo.update_crawl(crawl_process)
    return crawl_process


@celery_app.task(name="upload_html")
def upload_html(crawl_process: CrawlProcess):
    tmp_folder = "/html/"
    bucket_name = "html"

    client = Minio(
        "minio:9000",
        access_key=os.environ["MINIO_ROOT_USER"],
        secret_key=os.environ["MINIO_ROOT_PASSWORD"],
        secure=False,
    )

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    upload_root = pathlib.Path(f"{tmp_folder}{urlparse(crawl_process.config.url).netloc}")

    for html_file in upload_root.rglob("*.html"):
        client.fput_object(
            bucket_name, str(html_file).replace(tmp_folder, "", 1), str(html_file), content_type="text/html"
        )
        os.remove(html_file)
    shutil.rmtree(upload_root, ignore_errors=True)
    crawl_process.status = ProcessStatus.SUCCESS
    mongo.update_crawl(crawl_process)

