import unittest
from unittest.mock import patch, Mock

import requests

from services.carbon_calculator import CarbonCalculator, CarbonCalculatorError


class TestCarbonCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = CarbonCalculator()

    def test_empty_url_raises_value_error(self):
        with self.assertRaises(ValueError, msg="URL cannot be empty."):
            self.calculator.get_carbon_footprint("")

    @patch('services.carbon_calculator.requests.get')
    def test_valid_request_returns_json(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        url = "https://example.com"
        result = self.calculator.get_carbon_footprint(url)
        self.assertEqual(result, {"result": "success"})

    @patch('services.carbon_calculator.requests.get')
    def test_request_exception_raises_carbon_calculator_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Request error")

        with self.assertRaisesRegex(CarbonCalculatorError, "Request to Carbon Calculator API failed: Request error"):
            self.calculator.get_carbon_footprint("https://example.com")

    @patch('services.carbon_calculator.requests.get')
    def test_invalid_json_raises_carbon_calculator_error(self, mock_get):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with self.assertRaisesRegex(CarbonCalculatorError, "Failed to decode API response: Invalid JSON"):
            self.calculator.get_carbon_footprint("https://example.com")

    @patch('services.carbon_calculator.requests.get')
    def test_http_error_raises_carbon_calculator_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        with self.assertRaisesRegex(CarbonCalculatorError, "Request to Carbon Calculator API failed: 404 Not Found"):
            self.calculator.get_carbon_footprint("https://example.com")

    @patch('services.carbon_calculator.requests.get')
    def test_timeout_error_raises_carbon_calculator_error(self, mock_get):
        mock_get.side_effect = requests.Timeout("Request timed out")

        with self.assertRaisesRegex(CarbonCalculatorError, "Request to Carbon Calculator API failed: Request timed out"):
            self.calculator.get_carbon_footprint("https://example.com")

    # Optionally, you could add more tests for other exceptions raised by the requests library or other scenarios.


if __name__ == "__main__":
    unittest.main()
