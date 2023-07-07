import tldextract
from scrapy.exceptions import CloseSpider

from scrapy.spiders import CrawlSpider, Rule


def extract_domain(url: str):
    extract_result = tldextract.extract(url)
    return f"{extract_result.domain}.{extract_result.suffix}"


class MenesrSpider(CrawlSpider):
    name = "menesr"

    rules = (Rule(),)

    def __init__(self, url: str, *a, **kw):
        super().__init__(*a, **kw)
        self.allowed_domains = [extract_domain(url)]
        self.start_urls = [url]
        self.count = 0
        self.max_count = 5

        def parse(self, response):
            if self.count >= self.max_count:
                raise CloseSpider(reason="Reached maximum page count")
            super().parse(response)

            self.count += 1


if __name__ == "__main__":
    from scrapy.utils.project import get_project_settings

    from scrapy.crawler import CrawlerProcess

    crawler_settings = get_project_settings()
    crawler_settings.set("DEPTH_LIMIT", 1)
    process = CrawlerProcess(settings=crawler_settings)
    result = process.crawl(MenesrSpider, url="https://www.unistra.fr")
    process.start()
