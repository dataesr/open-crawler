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

logger = logging.getLogger(__name__)


def crawl(url: str, depth: int, limit: int, headers: dict):
    crawler_settings = get_project_settings()
    custom_settings = without_none_values(
        {"DEPTH_LIMIT": depth, "CLOSESPIDER_PAGECOUNT": limit, "CUSTOM_HEADERS": headers or {}}
    )
    crawler_settings.update(custom_settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(MenesrSpider, url=url)
    process.start()


@celery_app.task(name="crawl")
def start_crawl_process(url: str, depth: int, limit: int, headers: dict):
    p = Process(target=crawl, kwargs={"url": url, "depth": depth, "limit": limit, "headers": headers})
    p.start()
    p.join()


@celery_app.task(name="upload_html")
def upload_html(url: str):
    tmp_folder = "/html_files/"
    bucket_name = "html"

    client = Minio(
        "minio:9000",
        access_key=os.environ["MINIO_ROOT_USER"],
        secret_key=os.environ["MINIO_ROOT_PASSWORD"],
        secure=False,
    )

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    upload_root = pathlib.Path(f"{tmp_folder}{urlparse(url).netloc}")

    for html_file in upload_root.rglob("*.html"):
        client.fput_object(
            bucket_name, str(html_file).replace(tmp_folder, "", 1), str(html_file), content_type="text/html"
        )
        os.remove(html_file)
    shutil.rmtree(upload_root, ignore_errors=True)
