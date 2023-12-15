from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from app.models.process import CrawlProcess

class MenesrSpider(CrawlSpider):
    name = "menesr"
    rules = (Rule(),)
    use_playwright = False
    allowed_url = None
    allowed_domains = None
    first_real_url = None
    page_count = 0
    page_limit = 0
    depth_limit = 0

    def __init__(self, crawl_process: CrawlProcess, *a, **kw):
        self.use_playwright = crawl_process.config.parameters.use_playwright
        self.page_limit = crawl_process.config.parameters.limit
        self.depth_limit = crawl_process.config.parameters.depth
        self.start_urls = [crawl_process.config.url]
        self.crawl_process = crawl_process
        super().__init__(*a, **kw)

    
    def start_requests(self):
        for url in self.start_urls:
            meta = {
                "depth": 0,  # Set the initial depth to 0
            }
            if self.use_playwright:
                meta.update({
                    "playwright": True,
                    "playwright_page_methods": [
                        ("evaluate", 'window.scrollTo(0, document.body.scrollHeight)')
                    ],
                })
            yield Request(url, self.parse, meta=meta)

    def parse(self, response, **kwargs):
        # Crawl the links in the response page and continue to crawl the next page
        self.page_count += 1
        # Retrieve the depth of the current request
        depth = response.meta.get('depth', 0)
        if depth > self.depth_limit or self.page_limit != 0 and self.page_count > self.page_limit:
            self.crawler.engine.close_spider(self, 'page_or_depth_limit_reached')
            return

        links = LinkExtractor(allow=self.allowed_url).extract_links(response)
        for link in links:
            if self.use_playwright:
                yield Request(link.url, self.parse, meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        ("evaluate", 'window.scrollTo(0, document.body.scrollHeight)')
                    ]
                })
            else:
                # we don't need to add depth beacause the natif scrapy crawler already does it
                yield Request(link.url, self.parse)


if __name__ == "__main__":
    from scrapy.utils.project import get_project_settings

    from scrapy.crawler import CrawlerProcess

    crawler_settings = get_project_settings()
    crawler_settings.set("DEPTH_LIMIT", 1)
    process = CrawlerProcess(settings=crawler_settings)
    result = process.crawl(MenesrSpider, url="https://www.unistra.fr")
    process.start()
