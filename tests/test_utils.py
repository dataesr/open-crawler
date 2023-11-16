import unittest

from app.celery_broker.utils import assume_content_type


class TestAssumeContentType(unittest.TestCase):

    def test_html_extension(self):
        """Ensure 'text/html' is returned for .html extension."""
        self.assertEqual(assume_content_type("example.html"), "text/html")

    def test_json_extension(self):
        """Ensure 'application/json' is returned for .json extension."""
        self.assertEqual(assume_content_type("example.json"), "application/json")

    def test_unknown_file_extension(self):
        """Ensure default content type is returned for unknown extension."""
        self.assertEqual(assume_content_type("example.xyz"), "application/octet-stream")

    def test_no_file_extension(self):
        """Ensure default content type is returned for input without extension."""
        self.assertEqual(assume_content_type("example"), "application/octet-stream")

    def test_empty_string(self):
        """Ensure default content type is returned for empty input."""
        self.assertEqual(assume_content_type(""), "application/octet-stream")

    def test_multiple_periods(self):
        """Ensure content type is determined by the last part after a period."""
        self.assertEqual(assume_content_type("example.file.html"), "text/html")

    def test_mixed_case(self):
        """Ensure content type determination is case-insensitive."""
        self.assertEqual(assume_content_type("example.FILE.HTML"), "text/html")

if __name__ == "__main__":
    unittest.main()