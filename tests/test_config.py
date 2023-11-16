import unittest
from unittest.mock import patch

from app.config import get_settings, BaseConfig


class TestSettings(unittest.TestCase):

    def test_default_setting_is_development(self):
        with patch.dict(
            "os.environ", {}, clear=True
        ):  # Clearing the environment variables
            settings = get_settings()
            self.assertIsInstance(settings, BaseConfig)

    def test_baseconfig_attributes(self):
        config = BaseConfig()

        # Testing a sample attribute. Similarly, you can test other attributes.
        self.assertEqual(config.CRAWL_QUEUE_NAME, "crawl_queue")

        # Check if task_queues are constructed correctly
        self.assertTrue(
            any(q.name == config.CRAWL_QUEUE_NAME for q in config.task_queues)
        )

        # ... and so on for other attributes

    def test_baseconfig_get_method(self):
        config = BaseConfig()
        self.assertEqual(config.get("CRAWL_QUEUE_NAME"), "crawl_queue")


if __name__ == "__main__":
    unittest.main()
