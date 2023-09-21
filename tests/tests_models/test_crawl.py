import unittest

from models.crawl import (
    CrawlParameters,
    CrawlConfig,
    CrawlModel,
    ListCrawlResponse,
)
from models.enums import MetadataType
from models.metadata import MetadataConfig, AccessibilityModel


class TestCrawlParametersConfig(unittest.TestCase):
    def test_instantiation(self):
        params = CrawlParameters(depth=2, limit=400)
        config = CrawlConfig(
            url="http://example.com",
            parameters=params,
            metadata_config={MetadataType.ACCESSIBILITY: MetadataConfig()},
            headers={},
            tags=[],
        )

        self.assertEqual(config.url, "http://example.com")
        self.assertEqual(config.parameters.depth, 2)


class TestCrawlModel(unittest.TestCase):
    def test_default_values(self):
        config = CrawlConfig(
            url="http://example.com",
            parameters=CrawlParameters(depth=2, limit=400),
            metadata_config={MetadataType.ACCESSIBILITY: MetadataConfig()},
            headers={},
            tags=[],
        )
        crawl = CrawlModel(website_id="website_123", config=config)

        self.assertIsNotNone(crawl.id)
        self.assertIsNotNone(crawl.created_at)
        self.assertIsNone(crawl.accessibility)

    def test_enabled_metadata_property(self):
        config = CrawlConfig(
            url="http://example.com",
            parameters=CrawlParameters(depth=2, limit=400),
            metadata_config={
                MetadataType.ACCESSIBILITY: MetadataConfig(),
                MetadataType.TECHNOLOGIES: MetadataConfig(enabled=False),
            },
            headers={},
            tags=[],
        )
        crawl = CrawlModel(website_id="website_123", config=config)
        self.assertEqual(crawl.enabled_metadata, [MetadataType.ACCESSIBILITY])

    def test_init_tasks_method(self):
        config = CrawlConfig(
            url="http://example.com",
            parameters=CrawlParameters(depth=2, limit=400),
            metadata_config={MetadataType.ACCESSIBILITY: MetadataConfig()},
            headers={},
            tags=[],
        )
        crawl = CrawlModel(website_id="website_123", config=config)
        crawl.init_tasks()
        self.assertIsInstance(crawl.accessibility, AccessibilityModel)

    # Add more methods to test `update_task` and `update_status`


class TestListCrawlResponse(unittest.TestCase):
    def test_instantiation(self):
        config = CrawlConfig(
            url="http://example.com",
            parameters=CrawlParameters(depth=2, limit=400),
            metadata_config={MetadataType.ACCESSIBILITY: MetadataConfig()},
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
