# Define here the tests_models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from pathlib import Path
from urllib.parse import urlparse

from app.config import settings

from scrapy.downloadermiddlewares.defaultheaders import DefaultHeadersMiddleware
from scrapy.exceptions import IgnoreRequest
from scrapy.extensions.closespider import CloseSpider
from scrapy.utils.python import without_none_values


# useful for handling different item types with a single interface


class CustomCloseSpider(CloseSpider):
    def page_count(self, response, request, spider):
        if request.url.endswith("robots.txt"):
            return
        super().page_count(response, request, spider)


class CustomHeadersMiddleware(DefaultHeadersMiddleware):
    @classmethod
    def from_crawler(cls, crawler):
        headers = without_none_values(
            crawler.settings["DEFAULT_REQUEST_HEADERS"]
        )
        if custom_header := without_none_values(
            crawler.settings.get("CUSTOM_HEADERS")
        ):
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
        base_file_path = f"/{settings.LOCAL_FILES_PATH.strip('/')}/{spider.crawl_process.id}"
        file_name = response.url.split(f"{domain}")[-1].strip('/')
        if not file_name.endswith(".html"):
            file_name = f"{file_name}.html"
        if file_name == ".html":
            file_name = "index.html"
        return Path(
            f"{base_file_path}/{settings.HTML_FOLDER_NAME.strip('/')}/{file_name.lstrip('/')}"
        )

    def _save_html_locally(self, response, spider):
        file_path = self._format_file_path(response, spider)
        file_path.parent.mkdir(exist_ok=True, parents=True)
        file_path.write_text(response.text)

    def process_response(self, request, response, spider):

        if self.page_limit != 0 and self.current_page_count >= self.page_limit:
            raise IgnoreRequest(
                f"Page limit reached. Ignoring request {request}"
            )

        # Parse the domain from the response URL
        response_domain = urlparse(response.url).netloc

        # Check if the response domain is in the allowed domains
        if spider.allowed_domains is not None and response_domain not in spider.allowed_domains:
            raise IgnoreRequest(f"Domain not in allowed domains: {response.url}")

        # Check if the response URL matches the allowed URL
        if spider.allowed_url is not None and not response.url.rstrip('/').endswith(spider.allowed_url):
            raise IgnoreRequest(f"URL not allowed: {response.url}")

        if request.url.endswith("robots.txt"):
            return response

        if spider.first_real_url is None:
            # We should set the allowed_url and allowed_domains only once for the first request.
            # It is useful when we have a permanent redirection in the first request.
            spider.first_real_url = response.url
            parsed_url = urlparse(spider.first_real_url)
            if parsed_url.path:
                spider.allowed_url = parsed_url.path.strip('/')
            spider.allowed_domains = [parsed_url.netloc]

        if response.status == 200:
            self.current_page_count += 1
            self._save_html_locally(response, spider)

        return response


class MetadataMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_spider_output(self, response, result, spider):
        spider.crawl_process.save_url_for_metadata(
            response.url, response.meta["depth"]
        )
        return result

    async def process_spider_output_async(self, response, result, spider):
        spider.crawl_process.save_url_for_metadata(
            response.url, response.meta["depth"]
        )
        async for r in result or ():
            yield r
