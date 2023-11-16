import os
import unittest
from unittest.mock import patch, Mock

import requests.models

from app.config import settings
from app.services.responsiveness_calculator import (
    ResponsivenessCalculator,
    ResponsivenessCalculatorError,
)


class TestResponsivenessCalculator(unittest.TestCase):
    def setUp(self):
        # Set a fake API key for testing
        settings.GOOGLE_API_KEY = "FAKE_API_KEY"

    @patch("requests.post")
    def test_get_responsiveness(self, mock_post):
        # Mock a response from the ResponsivenessCalculator API
        mock_response_data = {
            "testStatus": "complete",
            "details": "details_here",
        }
        mock_post.return_value = Mock(json=lambda: mock_response_data)

        calculator = ResponsivenessCalculator()
        result = calculator.get_responsiveness(url="http://example.com")

        self.assertEqual(result, mock_response_data)
        mock_post.assert_called_with(
            calculator.base_url,
            data={"url": "http://example.com"},
            params={"key": "FAKE_API_KEY", "alt": "json"},
        )

    @patch("requests.post")
    def test_get_responsiveness_exception(self, mock_post):
        # Simulate an exception when calling requests.post
        mock_post.side_effect = Exception("Network error")

        calculator = ResponsivenessCalculator()
        with self.assertRaises(ResponsivenessCalculatorError):
            calculator.get_responsiveness(url="http://example.com")

    @patch("requests.post")
    def test_get_responsiveness_403_response(self, mock_post):
        # Mock a 403 status code response from the ResponsivenessCalculator API
        mock_response = requests.models.Response
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        calculator = ResponsivenessCalculator()
        with self.assertRaises(ResponsivenessCalculatorError):
            calculator.get_responsiveness(url="http://example.com")


if __name__ == "__main__":
    unittest.main()
