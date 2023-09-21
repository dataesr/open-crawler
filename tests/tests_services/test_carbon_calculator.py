import unittest
from unittest.mock import patch, Mock

from services.carbon_calculator import CarbonCalculator, CarbonCalculatorError


class TestCarbonCalculator(unittest.TestCase):
    @patch("requests.get")
    def test_get_carbon_footprint(self, mock_get):
        # Mock a response from the CarbonCalculator API
        mock_response_data = {"carbonFootprint": 100, "details": "details_here"}
        mock_get.return_value = Mock(json=lambda: mock_response_data)

        calculator = CarbonCalculator()
        result = calculator.get_carbon_footprint(url="http://example.com")

        self.assertEqual(result, mock_response_data)
        mock_get.assert_called_with(
            calculator.base_url, params={"url": "http://example.com"}
        )

    @patch("requests.get")
    def test_get_carbon_footprint_exception(self, mock_get):
        # Simulate an exception when calling requests.get
        mock_get.side_effect = Exception("Network error")

        calculator = CarbonCalculator()
        with self.assertRaises(CarbonCalculatorError):
            calculator.get_carbon_footprint(url="http://example.com")


if __name__ == "__main__":
    unittest.main()
