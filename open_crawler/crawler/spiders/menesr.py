import logging
from urllib.parse import urlparse

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger(__name__)


class MenesrSpider(CrawlSpider):
    name = "menesr"
    rules = (Rule(),)

    def __init__(self, url: str, *a, **kw):
        parsed_url = urlparse(url)
        logger.info(parsed_url.path)
        if parsed_url.path:
            self.rules = (Rule(LinkExtractor(allow=parsed_url.path)),)
        self.allowed_domains = [parsed_url.netloc]
        self.start_urls = [url]
        super().__init__(*a, **kw)


if __name__ == "__main__":
    from scrapy.utils.project import get_project_settings

    from scrapy.crawler import CrawlerProcess

    crawler_settings = get_project_settings()
    crawler_settings.set("DEPTH_LIMIT", 1)
    process = CrawlerProcess(settings=crawler_settings)
    result = process.crawl(MenesrSpider, url="https://www.unistra.fr")
    process.start()
