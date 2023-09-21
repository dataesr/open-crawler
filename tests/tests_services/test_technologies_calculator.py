import json
import unittest
from unittest.mock import patch, Mock

from services.technologies_calculator import TechnologiesCalculator, \
    TechnologiesError


class TestTechnologiesCalculator(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_technologies_success(self, mock_run):
        # Setup
        mock_result = Mock()
        mock_result.stdout = json.dumps({
            "technologies": [
                {"name": "Tech1", "confidence": 100},
                {"name": "Tech2", "confidence": 50}
            ]
        }).encode()
        mock_run.return_value = mock_result

        calc = TechnologiesCalculator()

        # Execution
        result = calc.get_technologies('http://example.com')

        # Assertion
        self.assertEqual(result, [{"name": "Tech1", "confidence": 100}])

    @patch('subprocess.run')
    def test_get_technologies_error(self, mock_run):
        # Setup
        mock_run.side_effect = Exception("Error running subprocess")

        calc = TechnologiesCalculator()

        # Execution & Assertion
        with self.assertRaises(TechnologiesError):
            calc.get_technologies('http://example.com')

    def test__be_agnostic(self):
        # Setup
        calc = TechnologiesCalculator()
        input_data = [
            {"name": "Tech1", "confidence": 100},
            {"name": "Tech2", "confidence": 50},
            {"name": "Tech3", "confidence": 100}
        ]

        # Execution
        result = calc._be_agnostic(input_data)

        # Assertion
        self.assertEqual(result, [
            {"name": "Tech1", "confidence": 100},
            {"name": "Tech3", "confidence": 100}
        ])

if __name__ == '__main__':
    unittest.main()