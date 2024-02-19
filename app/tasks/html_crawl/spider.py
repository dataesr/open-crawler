from urllib.parse import urlparse
from twisted.internet.error import DNSLookupError, TimeoutError

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.exceptions import CloseSpider

from app.services.logging import logger
from app.models.enums import ProcessStatus
from app.models.crawl import HTMLCrawlModel
from app.repositories.crawls import crawls
from app.repositories.files import files


PLAYWRIGHT_METADATA = {
    "playwright": True,
    "playwright_page_methods": [
        ("evaluate", 'window.scrollTo(0, document.body.scrollHeight)')
    ]
}


def store_html(crawl_id: str, parsed_url: urlparse, data):
    path = parsed_url.path
    stripped_path = path.strip('/')
    if not stripped_path.endswith(".html"):
        stripped_path = f"{stripped_path}.html"
    if stripped_path == ".html":
        stripped_path = "index.html"
    filename = f"{parsed_url.netloc}/{stripped_path}"
    files.store_html_file(
        crawl_id=crawl_id,
        key=filename.lstrip('/'),
        data=data)


class MenesrSpider(CrawlSpider):
    name = "menesr"
    rules = (Rule(),)
    use_playwright = False
    count = 0

    def __init__(self, crawl_id: str, url: str, crawl: HTMLCrawlModel, *a, **kw):
        parsed_url = urlparse(url)
        self.use_playwright = crawl.use_playwright
        self.url = url
        self.crawl = crawl
        self.crawl_id = crawl_id
        self.domains = [parsed_url.netloc]
        super().__init__(*a, **kw)

    def follow_links(self, links):
        meta = {}
        if self.use_playwright:
            meta.update(PLAYWRIGHT_METADATA)
        for link in links:
            yield Request(link.url, callback=self.parse, meta=meta)

    def closed(self, reason):
        if reason in ["finished", "limit", 'closespider_pagecount']:
            self.crawl.update(status=ProcessStatus.SUCCESS)
        else:
            self.crawl.update(status=ProcessStatus.ERROR)
        crawls.update_task(crawl_id=self.crawl_id,
                           task_name="html_crawl", task=self.crawl)

    def start_requests(self):
        # Force depth to 0 so scrapy does not ignore the first page
        # Set a longer timeout for the first page
        meta = {"depth": 0}
        if self.use_playwright:
            meta.update(PLAYWRIGHT_METADATA)
        yield Request(self.url, errback=self.parse_error, callback=self.parse_first, meta=meta)

    def parse_error(self, failure):
        # Fail crawl if DNSLookupError or HttpError on first page
        if failure.check(DNSLookupError):
            raise CloseSpider("DNSLookupError")
        if failure.check(TimeoutError):
            raise CloseSpider("TimeoutError")
        if failure.check(HttpError):
            if failure.value.response.status >= 400:
                raise CloseSpider("HttpError")

    def parse(self, response):
        if response.url.endswith("robots.txt"):
            return
        parsed_url = urlparse(response.url)
        store_html(self.crawl_id, parsed_url, response.text)
        self.crawl.urls.append(response.url)

        self.count += 1
        if self.crawl.limit == 1:
            raise CloseSpider("limit")

        if self.count < self.crawl.limit:
            max_links = self.crawl.limit - self.count
            links = LinkExtractor(
                allow_domains=self.domains).extract_links(response)
            yield from self.follow_links(links[:max_links])

    def parse_first(self, response):
        true_url = urlparse(response.url)
        self.domains.append(true_url.netloc)
        if true_url.netloc != self.domains[0]:
            self.crawl.redirection = true_url.netloc

        links = LinkExtractor(
            allow_domains=self.domains).extract_links(response)
        meta = {"depth": 0}
        if len(links) == 0:
            logger.debug("No links found, trying playwright")
            self.use_playwright = True
            meta.update(PLAYWRIGHT_METADATA)
            yield Request(self.url, callback=self.parse, meta=meta, dont_filter=True)
        else:
            yield Request(self.url, callback=self.parse, meta=meta, dont_filter=True)
