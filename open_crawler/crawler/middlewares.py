# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
import logging
import os
from pathlib import Path

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
    def __init__(self, page_limit: int, dir_path: str):
        self.page_limit = page_limit
        self.dir_path = dir_path
        self.current_page_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        page_limit = crawler.settings.get("CLOSESPIDER_PAGECOUNT", 0)
        dir_path = crawler.settings.get("TMP_HTML_DIR_PATH", f"{os.path.dirname(__file__)}/tmp")
        return cls(page_limit, dir_path)

    def _format_file_path(self, response, spider) -> Path:
        domain = spider.allowed_domains[0]
        file_path = response.url.split(f"{domain}/")[-1] or "index.html"
        file_path = f"{file_path}{'' if file_path.endswith('.html') else '.html'}"
        return Path(f"{self.dir_path}/{domain}/{datetime.date.today().strftime('%Y%m%d')}/{file_path}")

    def _save_html_locally(self, response, spider):
        file_path = self._format_file_path(response, spider)
        file_path.parent.mkdir(exist_ok=True, parents=True)
        file_path.write_text(response.text)

    def process_response(self, request, response, spider):
        if self.current_page_count >= self.page_limit:
            raise IgnoreRequest(f"Page limit reached. Ignoring request {request}")
        logger.debug(f"Processing request {request} response")
        if request.url.endswith("robots.txt"):
            return response
        if response.status == 200:
            self.current_page_count += 1
            self._save_html_locally(response, spider)

        return response
