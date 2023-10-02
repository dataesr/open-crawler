import json
import unittest
from unittest.mock import patch, Mock

from app.services.accessibility_best_practices_calculator import (
    LighthouseWrapper,
    LighthouseError,
    AccessibilityError,
    BestPracticesError,
)


class TestLighthouseWrapper(unittest.TestCase):
    @patch("subprocess.run")
    def test_get_accessibility(self, mock_run):
        # Mock a lighthouse response
        mock_response = {"categories": {"accessibility": {"score": 100}}}
        mock_run.return_value = Mock(
            stdout=json.dumps(mock_response).encode("utf-8")
        )
        wrapper = LighthouseWrapper()
        result = wrapper.get_accessibility(url="http://example.com")
        self.assertEqual(result, {"score": 100})

    @patch("subprocess.run")
    def test_get_best_practices(self, mock_run):
        # Mock a lighthouse response
        mock_response = {"categories": {"best-practices": {"score": 90}}}
        mock_run.return_value = Mock(
            stdout=json.dumps(mock_response).encode("utf-8")
        )
        wrapper = LighthouseWrapper()
        result = wrapper.get_best_practices(url="http://example.com")
        self.assertEqual(result, {"score": 90})

    @patch("subprocess.run")
    def test_get_accessibility_error(self, mock_run):
        mock_run.side_effect = LighthouseError
        wrapper = LighthouseWrapper()
        with self.assertRaises(AccessibilityError):
            wrapper.get_accessibility(url="http://example.com")

    @patch("subprocess.run")
    def test_get_best_practices_error(self, mock_run):
        mock_run.side_effect = LighthouseError
        wrapper = LighthouseWrapper()
        with self.assertRaises(BestPracticesError):
            wrapper.get_best_practices(url="http://example.com")


if __name__ == "__main__":
    unittest.main()
