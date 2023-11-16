import unittest

from app.models.crawl import CrawlModel, CrawlConfig, CrawlParameters
from app.models.enums import ProcessStatus, MetadataType
from app.models.metadata import MetadataConfig
from app.models.process import MetadataProcess, CrawlProcess


class TestMetadataProcess(unittest.TestCase):
    def test_default_values(self):
        meta = MetadataProcess()
        self.assertEqual(meta.urls, [])
        self.assertEqual(meta.status, ProcessStatus.PENDING)
        self.assertTrue(meta.to_save)

    def test_set_status_method(self):
        meta = MetadataProcess()
        meta.set_status(ProcessStatus.SUCCESS)
        self.assertEqual(meta.status, ProcessStatus.SUCCESS)
        self.assertTrue(meta.to_save)


class TestCrawlProcess(unittest.TestCase):
    def test_from_model_classmethod(self):
        model = CrawlModel(
            id="crawl_123",
            website_id="website_123",
            config=CrawlConfig(
                url="http://example.com",
                parameters=CrawlParameters(depth=2, limit=400),
                metadata_config={MetadataType.LIGHTHOUSE: MetadataConfig()},
                headers={},
                tags=[],
            ),
        )
        process = CrawlProcess.from_model(model)
        self.assertEqual(process.id, "crawl_123")
        self.assertEqual(process.website_id, "website_123")

    def test_enabled_metadata_property(self):
        config = CrawlConfig(
            url="http://example.com",
            parameters=CrawlParameters(depth=2, limit=400),
            metadata_config={
                MetadataType.LIGHTHOUSE: MetadataConfig(),
                MetadataType.TECHNOLOGIES: MetadataConfig(enabled=False),
            },
            headers={},
            tags=[],
        )
        process = CrawlProcess(
            id="crawl_123", website_id="website_123", config=config
        )
        self.assertEqual(process.enabled_metadata, [MetadataType.LIGHTHOUSE])

    # Write more test methods for `save_url_for_metadata`, `set_from`, `set_metadata_status`, and `metadata_needs_save`.


if __name__ == "__main__":
    unittest.main()
