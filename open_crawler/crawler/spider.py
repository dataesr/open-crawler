from urllib.parse import urlparse

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from models.process import CrawlProcess


class MenesrSpider(CrawlSpider):
    name = "menesr"
    rules = (Rule(),)

    def __init__(self, crawl_process: CrawlProcess, *a, **kw):
        parsed_url = urlparse(crawl_process.config.url)
        if parsed_url.path:
            self.rules = (Rule(LinkExtractor(allow=parsed_url.path)),)
        self.allowed_domains = [parsed_url.netloc]
        self.start_urls = [crawl_process.config.url]
        self.crawl_process = crawl_process
        super().__init__(*a, **kw)


if __name__ == "__main__":
    from scrapy.utils.project import get_project_settings

    from scrapy.crawler import CrawlerProcess

    crawler_settings = get_project_settings()
    crawler_settings.set("DEPTH_LIMIT", 1)
    process = CrawlerProcess(settings=crawler_settings)
    result = process.crawl(MenesrSpider, url="https://www.unistra.fr")
    process.start()
