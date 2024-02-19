import unittest
from unittest.mock import MagicMock
from urllib.parse import urlparse

from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.spiders import Rule

from app.tasks.html_crawl.spider import MenesrSpider


class TestMenesrSpider(unittest.TestCase):
    def setUp(self):
        # Mocking CrawlProcess instance
        self.mock_crawl_process = MagicMock()
        self.mock_crawl_process.config.url = "http://example.com/path/subpath"

    def test_init_without_path(self):
        # Mocking URL without a path
        self.mock_crawl_process.config.url = "http://example.com/"
        spider = MenesrSpider(self.mock_crawl_process)

        self.assertEqual(spider.start_urls, ["http://example.com/"])
        self.assertTrue(isinstance(spider.rules, tuple))

    def test_init_with_path(self):
        spider = MenesrSpider(self.mock_crawl_process)

        # Checking initialized values
        self.assertEqual(
            spider.start_urls, [self.mock_crawl_process.config.url]
        )
        self.assertEqual(len(spider.rules), 1)  # one rule
        self.assertTrue(isinstance(spider.rules[0], Rule))

    def test_name(self):
        self.assertEqual(MenesrSpider.name, "menesr")

    def test_start_requests(self):
        self.mock_crawl_process.config.url = "http://www.example.com/"
        spider = MenesrSpider(self.mock_crawl_process)
        request = next(spider.start_requests())
        self.assertEqual(request.url, 'http://www.example.com/')
        self.assertEqual(request.callback, spider.parse)

    def test_parse(self):
        self.mock_crawl_process.config.url = "http://www.example.com/"
        url = self.mock_crawl_process.config.url
        spider = MenesrSpider(self.mock_crawl_process)
        spider.depth_limit = 1
        spider.page_limit = 2
        request = Request(url)
        body = ('<html><a href="/recherche/lactualite-de-la-recherche"><span>L\'actualité de la '
                'recherche</span></a></html>').encode('utf-8')
        response = HtmlResponse(
            url=url, body=body, encoding='utf-8', request=request)
        result = next(spider.parse(response))
        assert result.url == 'http://www.example.com/recherche/lactualite-de-la-recherche'
        # Add assertions here to check the result


if __name__ == "__main__":
    unittest.main()
