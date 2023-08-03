# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import os
from pathlib import Path
from urllib.parse import urlparse

from scrapy.downloadermiddlewares.defaultheaders import DefaultHeadersMiddleware
from scrapy.exceptions import IgnoreRequest
from scrapy.extensions.closespider import CloseSpider
from scrapy.utils.python import without_none_values

# useful for handling different item types with a single interface

logger = logging.getLogger(__name__)


class CustomCloseSpider(CloseSpider):
    def page_count(self, response, request, spider):
        if request.url.endswith("robots.txt"):
            return
        super().page_count(response, request, spider)


class CustomHeadersMiddleware(DefaultHeadersMiddleware):
    @classmethod
    def from_crawler(cls, crawler):
        headers = without_none_values(crawler.settings["DEFAULT_REQUEST_HEADERS"])
        if custom_header := without_none_values(crawler.settings.get("CUSTOM_HEADERS")):
            headers.update(custom_header)
        return cls(headers.items())


class HtmlStorageMiddleware:
    def __init__(self, page_limit: int):
        self.page_limit = page_limit
        self.current_page_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        page_limit = crawler.settings.get("CLOSESPIDER_PAGECOUNT", 0)
        return cls(page_limit)

    def _format_file_path(self, response, spider) -> Path:
        domain = spider.allowed_domains[0]
        if not spider.crawl_process.base_file_path:
            spider.crawl_process.base_file_path = (
                f"{os.environ['LOCAL_FILES_PATH']},{domain}/"
                f"{spider.crawl_process.date.isoformat()}-{urlparse(response.url).scheme}"
            )
        file_name = response.url.split(f"{domain}/")[-1] or "index.html"
        if not file_name.endswith(".html"):
            file_name = f"{file_name}.html"
        return Path(f"{spider.crawl_process.base_file_path}/{os.environ['HTML_FOLDER_NAME']}/{file_name}")

    def _save_html_locally(self, response, spider):
        file_path = self._format_file_path(response, spider)
        file_path.parent.mkdir(exist_ok=True, parents=True)
        file_path.write_text(response.text)

    def process_response(self, request, response, spider):
        if self.page_limit != 0 and self.current_page_count >= self.page_limit:
            raise IgnoreRequest(f"Page limit reached. Ignoring request {request}")
        if request.url.endswith("robots.txt"):
            return response
        if response.status == 200:
            self.current_page_count += 1
            self._save_html_locally(response, spider)

        return response


class MetadataMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_spider_output(self, response, result, spider):
        spider.crawl_process.save_url_for_metadata(response.url, response.meta["depth"])
        return result

    async def process_spider_output_async(self, response, result, spider):
        spider.crawl_process.save_url_for_metadata(response.url, response.meta["depth"])
        async for r in result or ():
            yield r
