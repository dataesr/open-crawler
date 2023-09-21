import unittest
from unittest.mock import MagicMock
from urllib.parse import urlparse

from scrapy.spiders import Rule

from crawler.spiders.menesr import MenesrSpider


class TestMenesrSpider(unittest.TestCase):

    def setUp(self):
        # Mocking CrawlProcess instance
        self.mock_crawl_process = MagicMock()
        self.mock_crawl_process.config.url = 'http://example.com/path/subpath'

    def test_init_without_path(self):
        # Mocking URL without a path
        self.mock_crawl_process.config.url = 'http://example.com/'
        spider = MenesrSpider(self.mock_crawl_process)

        self.assertEqual(spider.allowed_domains, ['example.com'])
        self.assertEqual(spider.start_urls, ['http://example.com/'])
        self.assertTrue(isinstance(spider.rules, tuple))

    def test_init_with_path(self):
        spider = MenesrSpider(self.mock_crawl_process)

        # Checking initialized values
        parsed_url = urlparse(self.mock_crawl_process.config.url)
        self.assertEqual(spider.allowed_domains, [parsed_url.netloc])
        self.assertEqual(spider.start_urls,
                         [self.mock_crawl_process.config.url])
        self.assertEqual(len(spider.rules), 1)  # one rule
        self.assertTrue(isinstance(spider.rules[0], Rule))

    def test_name(self):
        self.assertEqual(MenesrSpider.name, "menesr")


if __name__ == '__main__':
    unittest.main()