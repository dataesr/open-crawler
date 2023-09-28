import unittest
from unittest.mock import patch, MagicMock

from crawler.middlewares import (
    CustomCloseSpider,
    CustomHeadersMiddleware,
    HtmlStorageMiddleware,
    MetadataMiddleware,
)


class BaseTest(unittest.TestCase):
    def mock_request(self, url="http://example.com/test"):
        request = MagicMock()
        request.url = url
        return request

    def mock_response(
        self,
        url="http://example.com/test",
        depth=1,
        status=200,
        text="mocked_content",
    ):
        response = MagicMock()
        response.url = url
        response.meta = {"depth": depth}
        response.status = status
        response.text = text
        return response

    def mock_spider(self, domain="example.com", id=1):
        spider = MagicMock()
        spider.allowed_domains = [domain]
        spider.crawl_process = MagicMock(id=id)
        return spider


class TestCustomCloseSpider(BaseTest):
    @patch("crawler.middlewares.CloseSpider.page_count")
    def test_page_count_with_robots_txt(self, mocked_page_count):
        middleware = CustomCloseSpider(MagicMock())
        middleware.page_count(
            self.mock_response(),
            self.mock_request(url="http://example.com/robots.txt"),
            self.mock_spider(),
        )
        mocked_page_count.assert_not_called()

    @patch("crawler.middlewares.CloseSpider.page_count")
    def test_page_count_without_robots_txt(self, mocked_page_count):
        middleware = CustomCloseSpider(MagicMock())
        middleware.page_count(
            self.mock_response(), self.mock_request(), self.mock_spider()
        )
        mocked_page_count.assert_called()


class TestCustomHeadersMiddleware(unittest.TestCase):
    def test_from_crawler(self):
        mock_crawler = MagicMock()
        mock_crawler.settings = {
            "DEFAULT_REQUEST_HEADERS": {
                "Header1": "Value1",
                "Header2": None,
                "Header3": "Value3",
            },
            "CUSTOM_HEADERS": {"HeaderA": "ValueA", "HeaderB": None},
        }
        middleware = CustomHeadersMiddleware.from_crawler(mock_crawler)
        expected_headers = [
            ("Header1", "Value1"),
            ("Header3", "Value3"),
            ("HeaderA", "ValueA"),
        ]
        self.assertEqual(list(middleware._headers), expected_headers)


class TestHtmlStorageMiddleware(BaseTest):
    def setUp(self):
        self.middleware = HtmlStorageMiddleware(5)

    @patch("crawler.middlewares.Path.write_text")
    @patch("crawler.middlewares.Path.mkdir")
    @patch.dict(
        "os.environ", {"LOCAL_FILES_PATH": "/tmp", "HTML_FOLDER_NAME": "html"}
    )
    def test_process_response(self, mock_mkdir, mock_write_text):
        mock_response = self.mock_response()
        result = self.middleware.process_response(
            self.mock_request(), mock_response, self.mock_spider()
        )
        mock_mkdir.assert_called_once()
        mock_write_text.assert_called_once_with(self.mock_response().text)
        self.assertEqual(result, mock_response)

    @patch("crawler.middlewares.Path.write_text")
    @patch("crawler.middlewares.Path.mkdir")
    @patch.dict(
        "os.environ", {"LOCAL_FILES_PATH": "/tmp", "HTML_FOLDER_NAME": "html"}
    )
    def test_robots_txt_skip(self, mock_mkdir, mock_write_text):
        mock_response = self.mock_response(url="http://example.com/robots.txt")
        result = self.middleware.process_response(
            self.mock_request(url="http://example.com/robots.txt"),
            mock_response,
            self.mock_spider(),
        )
        mock_mkdir.assert_not_called()
        mock_write_text.assert_not_called()
        self.assertEqual(result, mock_response)

    def test_page_limit_reached(self):
        self.middleware.page_limit = 1
        self.middleware.current_page_count = 1
        with self.assertRaises(Exception) as context:
            self.middleware.process_response(
                None, self.mock_response(), self.mock_spider()
            )
        self.assertIn("Page limit reached", str(context.exception))

    def test_from_crawler(self):
        mock_crawler = MagicMock()
        mock_crawler.settings.get.return_value = 10
        middleware_instance = HtmlStorageMiddleware.from_crawler(mock_crawler)
        self.assertIsInstance(middleware_instance, HtmlStorageMiddleware)
        self.assertEqual(middleware_instance.page_limit, 10)


class TestMetadataMiddleware(BaseTest):
    def setUp(self):
        self.middleware = MetadataMiddleware()

    def test_process_spider_output(self):
        result = [MagicMock(), MagicMock()]
        mock_spider = self.mock_spider()
        modified_result = list(
            self.middleware.process_spider_output(
                self.mock_response(), result, mock_spider
            )
        )
        mock_spider.crawl_process.save_url_for_metadata.assert_called_once_with(
            self.mock_response().url, self.mock_response().meta["depth"]
        )
        self.assertEqual(modified_result, result)

    def test_from_crawler(self):
        middleware_instance = MetadataMiddleware.from_crawler(MagicMock())
        self.assertIsInstance(middleware_instance, MetadataMiddleware)


if __name__ == "__main__":
    unittest.main()
