import unittest

from pydantic import ValidationError

from app.models.enums import ProcessStatus
from app.models.metadata import MetadataConfig, MetadataTask, AccessibilityModel


class TestMetadataConfig(unittest.TestCase):
    def test_default_values(self):
        config = MetadataConfig()

        self.assertTrue(config.enabled)
        self.assertEqual(config.depth, 0)

    def test_depth_constraints(self):
        # Test that negative values raise a ValidationError
        with self.assertRaises(ValidationError):
            MetadataConfig(depth=-1)


class TestMetadataTask(unittest.TestCase):
    def test_instantiation(self):
        task = MetadataTask()
        self.assertIsNone(task.task_id)
        self.assertIsNone(task.started_at)
        self.assertIsNone(task.finished_at)
        self.assertEqual(task.status, ProcessStatus.PENDING)


class TestAccessibilityModel(unittest.TestCase):
    def test_default_values(self):
        model = AccessibilityModel()

        self.assertIsNone(model.score)
        self.assertIsNone(model.task_id)
        self.assertIsNone(model.started_at)
        self.assertIsNone(model.finished_at)
        self.assertEqual(model.status, ProcessStatus.PENDING)


if __name__ == "__main__":
    unittest.main()
