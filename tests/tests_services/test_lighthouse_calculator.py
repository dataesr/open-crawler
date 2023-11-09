import json
import unittest
from unittest.mock import patch, Mock

from services.lighthouse_calculator import (
    LighthouseCalculator,
    LighthouseError,
)


class TestLighthouseCalculator(unittest.TestCase):
    @patch("subprocess.run")
    def test_get_lighthouse(self, mock_run):
        # Mock a lighthouse response
        mock_response = {"categories": {"accessibility": {"score": 100}}}
        mock_run.return_value = Mock(
            stdout=json.dumps(mock_response).encode("utf-8")
        )
        wrapper = LighthouseCalculator()
        result = wrapper.get_lighthouse(url="http://example.com")
        self.assertEqual(result, {"score": 100})

    @patch("subprocess.run")
    def test_get_lighthouse_error(self, mock_run):
        mock_run.side_effect = LighthouseError
        wrapper = LighthouseCalculator()
        with self.assertRaises(LighthouseError):
            wrapper.get_lighthouse(url="http://example.com")


if __name__ == "__main__":
    unittest.main()
