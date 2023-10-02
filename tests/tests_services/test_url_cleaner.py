import unittest

from app.services.url_cleaner import clean_url


class TestCleanUrl(unittest.TestCase):
    def test_clean_url_no_changes_needed(self):
        self.assertEqual(clean_url("http://example.com"), "http://example.com")

    def test_clean_url_remove_trailing_slash(self):
        self.assertEqual(clean_url("http://example.com/"), "http://example.com")

    def test_clean_url_remove_spaces(self):
        self.assertEqual(clean_url("http://exa mple.com"), "http://example.com")

    def test_clean_url_encode_decode(self):
        # This test is essentially verifying that encoding and immediately decoding a string does not change it.
        # The functionality might seem redundant, but it is present in your provided function.
        self.assertEqual(clean_url("http://example.com"), "http://example.com")

    def test_clean_url_combined(self):
        self.assertEqual(
            clean_url("http://exa mple.com/ "), "http://example.com"
        )


if __name__ == "__main__":
    unittest.main()
