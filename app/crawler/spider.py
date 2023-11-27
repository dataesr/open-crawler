from urllib.parse import urlparse

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from app.models.process import CrawlProcess


class MenesrSpider(CrawlSpider):
    name = "menesr"
    rules = (Rule(),)
    use_playwright = False

    def __init__(self, crawl_process: CrawlProcess, *a, **kw):
        parsed_url = urlparse(crawl_process.config.url)
        if parsed_url.path:
            self.rules = (Rule(LinkExtractor(allow=parsed_url.path)),)
        self.allowed_domains = [parsed_url.netloc]
        self.start_urls = [crawl_process.config.url]
        self.crawl_process = crawl_process
        self.use_playwright = crawl_process.config.parameters.use_playwright
        super().__init__(*a, **kw)

    def start_requests(self):
        for url in self.start_urls:
            if self.use_playwright:
                yield Request(url, self.parse, meta={
                    'depth': 0, # Set the initial depth to 0
                    "playwright": True,
                    "playwright_page_methods": [
                        ("evaluate", 'window.scrollTo(0, document.body.scrollHeight)')
                    ]
                })
            else:
                yield Request(url, self.parse)


    def parse(self, response, **kwargs):
        # Crawl the links in the response page and continue to crawl the next page
        links = LinkExtractor().extract_links(response)
        for link in links:
            if self.use_playwright:
                yield Request(link.url, self.parse, meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        ("evaluate", 'window.scrollTo(0, document.body.scrollHeight)')
                    ]
                })
            else:
                yield Request(link.url)


if __name__ == "__main__":
    from scrapy.utils.project import get_project_settings

    from scrapy.crawler import CrawlerProcess

    crawler_settings = get_project_settings()
    crawler_settings.set("DEPTH_LIMIT", 1)
    process = CrawlerProcess(settings=crawler_settings)
    result = process.crawl(MenesrSpider, url="https://www.unistra.fr")
    process.start()
