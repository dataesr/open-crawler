import unittest
from datetime import datetime, timezone, timedelta

from models.crawl import CrawlConfig
from models.metadata import MetadataConfig
from models.website import WebsiteModel, ListWebsiteResponse


class TestWebsiteModel(unittest.TestCase):
    def test_default_values(self):
        website = WebsiteModel(
            url="http://example.com",
            depth=2,
            limit=400,
            accessibility=MetadataConfig(),
            technologies_and_trackers=MetadataConfig(),
            responsiveness=MetadataConfig(),
            good_practices=MetadataConfig(),
            carbon_footprint=MetadataConfig(),
            headers={},
            tags=[],
            crawl_every=30,
        )

        self.assertIsNotNone(website.id)
        self.assertIsNotNone(website.created_at)
        self.assertIsNotNone(website.updated_at)
        self.assertIsNone(website.next_crawl_at)
        self.assertIsNone(website.last_crawl)

    def test_to_config_method(self):
        website = WebsiteModel(
            url="http://example.com",
            depth=2,
            limit=400,
            accessibility=MetadataConfig(),
            technologies_and_trackers=MetadataConfig(),
            responsiveness=MetadataConfig(),
            good_practices=MetadataConfig(),
            carbon_footprint=MetadataConfig(),
            headers={},
            tags=["test"],
            crawl_every=30,
        )
        config = website.to_config()
        self.assertIsInstance(config, CrawlConfig)
        self.assertEqual(config.url, "http://example.com")
        self.assertEqual(config.parameters.depth, 2)
        self.assertEqual(config.parameters.limit, 400)
        self.assertEqual(config.tags, ["test"])

    def test_refresh_next_crawl_date(self):
        website = WebsiteModel(
            url="http://example.com",
            depth=2,
            limit=400,
            accessibility=MetadataConfig(),
            technologies_and_trackers=MetadataConfig(),
            responsiveness=MetadataConfig(),
            good_practices=MetadataConfig(),
            carbon_footprint=MetadataConfig(),
            headers={},
            tags=[],
            crawl_every=30,
        )
        website.refresh_next_crawl_date()
        self.assertIsNotNone(website.next_crawl_at)
        self.assertTrue(website.next_crawl_at > french_datetime())


class TestListWebsiteResponse(unittest.TestCase):
    def test_instantiation(self):
        website1 = WebsiteModel(
            url="http://example1.com",
            depth=2,
            limit=400,
            accessibility=MetadataConfig(),
            technologies_and_trackers=MetadataConfig(),
            responsiveness=MetadataConfig(),
            good_practices=MetadataConfig(),
            carbon_footprint=MetadataConfig(),
            headers={},
            tags=[],
            crawl_every=30,
        )
        website2 = WebsiteModel(
            url="http://example2.com",
            depth=3,
            limit=500,
            accessibility=MetadataConfig(enabled=False),
            technologies_and_trackers=MetadataConfig(),
            responsiveness=MetadataConfig(),
            good_practices=MetadataConfig(),
            carbon_footprint=MetadataConfig(),
            headers={},
            tags=["sample"],
            crawl_every=40,
        )

        response = ListWebsiteResponse(
            count=2,
            data=[website1, website2],
            tags=["test"],
            status=["pending"],
        )

        self.assertEqual(response.count, 2)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.tags, ["test"])
        self.assertEqual(response.status, ["pending"])


if __name__ == "__main__":
    unittest.main()
