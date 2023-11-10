import unittest
from datetime import timedelta

from pydantic import ValidationError

from app.celery_broker.utils import french_datetime
from app.models.metadata import MetadataConfig
from app.models.request import CreateWebsiteRequest, UpdateWebsiteRequest
from app.models.website import WebsiteModel


class TestCreateWebsiteRequest(unittest.TestCase):
    def test_default_values(self):
        request = CreateWebsiteRequest(url="http://example.com")

        self.assertEqual(request.url, "http://example.com")
        self.assertEqual(request.depth, 2)
        self.assertEqual(request.limit, 400)
        self.assertEqual(request.headers, {})
        self.assertEqual(request.tags, [])
        self.assertEqual(request.crawl_every, 30)

        # Assuming MetadataConfig has a property called "enabled"
        self.assertTrue(request.accessibility.enabled)
        self.assertFalse(request.technologies_and_trackers.enabled)
        self.assertFalse(request.responsiveness.enabled)
        self.assertFalse(request.good_practices.enabled)
        self.assertFalse(request.carbon_footprint.enabled)

    def test_depth_field_constraints(self):
        with self.assertRaises(ValidationError):
            CreateWebsiteRequest(url="http://example.com", depth=-1)

    def test_limit_field_constraints(self):
        with self.assertRaises(ValidationError):
            CreateWebsiteRequest(url="http://example.com", limit=-1)

    def test_crawl_every_field_constraints(self):
        with self.assertRaises(ValidationError):
            CreateWebsiteRequest(url="http://example.com", crawl_every=-1)

    def test_to_website_model(self):
        request = CreateWebsiteRequest(url="http://example.com")
        website = request.to_website_model()

        self.assertIsInstance(website, WebsiteModel)
        self.assertEqual(website.url, "http://example.com")
        self.assertEqual(website.depth, 2)
        self.assertTrue(
            (
                (french_datetime() + timedelta(days=30)).replace(
                    hour=0, minute=0, second=0
                )
                - website.next_crawl_at
            ).seconds
            < 1
        )


class TestUpdateWebsiteRequest(unittest.TestCase):
    def test_default_values(self):
        request = UpdateWebsiteRequest()

        self.assertIsNone(request.depth)
        self.assertIsNone(request.limit)
        self.assertIsNone(request.headers)
        self.assertIsNone(request.tags)
        self.assertIsNone(request.crawl_every)
        self.assertIsNone(request.next_crawl_at)

        # For MetadataConfig properties
        self.assertIsNone(request.accessibility)
        self.assertIsNone(request.technologies_and_trackers)
        self.assertIsNone(request.responsiveness)
        self.assertIsNone(request.good_practices)
        self.assertIsNone(request.carbon_footprint)

    def test_crawl_every_field_constraints(self):
        with self.assertRaises(ValidationError):
            UpdateWebsiteRequest(crawl_every=-1)

    def test_assigning_values(self):
        now = french_datetime()
        request = UpdateWebsiteRequest(
            depth=3,
            limit=500,
            headers={"User-Agent": "test-agent"},
            tags=["example", "test"],
            crawl_every=20,
            next_crawl_at=now,
            accessibility=MetadataConfig(enabled=True),
        )

        self.assertEqual(request.depth, 3)
        self.assertEqual(request.limit, 500)
        self.assertEqual(request.headers, {"User-Agent": "test-agent"})
        self.assertEqual(request.tags, ["example", "test"])
        self.assertEqual(request.crawl_every, 20)
        self.assertEqual(request.next_crawl_at, now)
        self.assertTrue(request.accessibility.enabled)


if __name__ == "__main__":
    unittest.main()
