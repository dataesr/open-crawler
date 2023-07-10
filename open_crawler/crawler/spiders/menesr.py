from urllib.parse import urlparse

from scrapy.spiders import CrawlSpider, Rule


class MenesrSpider(CrawlSpider):
    name = "menesr"
    rules = (Rule(),)

    def __init__(self, url: str, *a, **kw):
        super().__init__(*a, **kw)
        self.allowed_domains = [urlparse(url).netloc]
        self.start_urls = [url]


if __name__ == "__main__":
    from scrapy.utils.project import get_project_settings

    from scrapy.crawler import CrawlerProcess

    crawler_settings = get_project_settings()
    crawler_settings.set("DEPTH_LIMIT", 1)
    process = CrawlerProcess(settings=crawler_settings)
    result = process.crawl(MenesrSpider, url="https://www.unistra.fr")
    process.start()
