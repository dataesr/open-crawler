import scrapy

from open_crawler.crawler.items import DemoItem


class DemoSpider(scrapy.Spider):
    name = "demo_spider"
    start_urls = ["http://www.google.com"]

    def parse(self, response):
        # extract url
        url = response.url

        # extract html content
        html = response.body

        item = DemoItem()
        item["url"] = url
        item["html"] = html

        # return the item to the pipeline
        yield item
