import unittest

from app.models.crawl import (
    CrawlParameters,
    CrawlConfig,
    CrawlModel,
    ListCrawlResponse,
)
from app.models.enums import MetadataType
from app.models.metadata import MetadataConfig, LighthouseModel


class TestCrawlParametersConfig(unittest.TestCase):
    def test_instantiation(self):
        params = CrawlParameters(depth=2, limit=400, use_playwright=False)
        config = CrawlConfig(
            url="http://example.com",
            parameters=params,
            metadata_config={MetadataType.LIGHTHOUSE: MetadataConfig()},
            headers={},
            tags=[],
        )

        self.assertEqual(config.url, "http://example.com")
        self.assertEqual(config.parameters.depth, 2)


class TestCrawlModel(unittest.TestCase):
    def test_default_values(self):
        config = CrawlConfig(
            url="http://example.com",
            parameters=CrawlParameters(depth=2, limit=400, use_playwright=False),
            metadata_config={MetadataType.LIGHTHOUSE: MetadataConfig()},
            headers={},
            tags=[],
        )
        crawl = CrawlModel(website_id="website_123", config=config)

        self.assertIsNotNone(crawl.id)
        self.assertIsNotNone(crawl.created_at)
        self.assertIsNone(crawl.lighthouse)

    def test_enabled_metadata_property(self):
        config = CrawlConfig(
            url="http://example.com",
            parameters=CrawlParameters(depth=2, limit=400, use_playwright=True),
            metadata_config={
                MetadataType.LIGHTHOUSE: MetadataConfig(),
                MetadataType.TECHNOLOGIES: MetadataConfig(enabled=False),
            },
            headers={},
            tags=[],
        )
        crawl = CrawlModel(website_id="website_123", config=config)
        self.assertEqual(crawl.enabled_metadata, [MetadataType.LIGHTHOUSE])

    def test_init_tasks_method(self):
        config = CrawlConfig(
            url="http://example.com",
            parameters=CrawlParameters(depth=2, limit=400, use_playwright=True),
            metadata_config={MetadataType.LIGHTHOUSE: MetadataConfig()},
            headers={},
            tags=[],
        )
        crawl = CrawlModel(website_id="website_123", config=config)
        crawl.init_tasks()
        self.assertIsInstance(crawl.lighthouse, LighthouseModel)

    # Add more methods to test `update_task` and `update_status`


class TestListCrawlResponse(unittest.TestCase):
    def test_instantiation(self):
        config = CrawlConfig(
            url="http://example.com",
            parameters=CrawlParameters(depth=2, limit=400, use_playwright=True),
            metadata_config={MetadataType.LIGHTHOUSE: MetadataConfig()},
            headers={},
            tags=[],
        )
        crawl1 = CrawlModel(website_id="website_123", config=config)
        crawl2 = CrawlModel(website_id="website_124", config=config)
        response = ListCrawlResponse(count=2, data=[crawl1, crawl2])

        self.assertEqual(response.count, 2)
        self.assertEqual(len(response.data), 2)


if __name__ == "__main__":
    unittest.main()
