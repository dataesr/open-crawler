# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging

from scrapy import signals
from scrapy.downloadermiddlewares.defaultheaders import DefaultHeadersMiddleware
from scrapy.exceptions import IgnoreRequest
from scrapy.extensions.closespider import CloseSpider
from scrapy.utils.python import without_none_values

# useful for handling different item types with a single interface

logger = logging.getLogger(__name__)


class CrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class CrawlerDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class CustomCloseSpider(CloseSpider):
    def __init__(self, crawler):
        super().__init__(crawler)

        # crawler.signals.connect(self.received, signal=signals.request_received)
        # crawler.signals.connect(self.scheduled, signal=signals.request_scheduled)
        # crawler.signals.connect(self.reached, signal=signals.request_reached_downloader)
        # crawler.signals.connect(self.dropped, signal=signals.request_dropped)
        # crawler.signals.connect(self.left, signal=signals.request_left_downloader)

    def page_count(self, response, request, spider):
        self.counter["pagecount"] += 1
        if self.counter["pagecount"] == self.close_on["pagecount"]:
            # self.crawler.engine.downloader._slot_gc_loop.stop()
            for slot in self.crawler.engine.downloader.slots.values():
                slot.active = set()
            while self.crawler.engine.slot.scheduler.dqs:
                self.crawler.engine.slot.scheduler.dqs.pop()
                self.crawler.stats.inc_value("disk_queue/cleared")
            while self.crawler.engine.slot.scheduler.mqs:
                self.crawler.engine.slot.scheduler.mqs.pop()
                self.crawler.stats.inc_value("memory_queue/cleared")
            self.crawler.engine.close_spider(spider, "closespider_pagecount")
            # while self.crawler.engine.slot.inprogress:
            #     self.crawler.engine.slot.inprogress.pop()
        # logger.debug(f"Scheduler request count: {len(spider.crawler.engine.slot.scheduler)}")
        # logger.debug(f"InProgress request count: {len(spider.crawler.engine.slot.inprogress)}")
        # while spider.crawler.engine.slot

    # def scheduled(self, request, spider):
    #     logger.debug(f"{request} scheduled.")
    #
    # def dropped(self, request, spider):
    #     logger.debug(f"{request} dropped.")
    #
    # def received(self, request, spider):
    #     logger.debug(f"{request} received.")
    #
    # def reached(self, request, spider):
    #     logger.debug(f"{request} reached.")
    #
    # def left(self, request, spider):
    #     logger.debug(f"{request} left.")


class PageLimitMiddleware:
    def __init__(self, page_limit):
        self.page_limit = page_limit
        self.current_page_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        page_limit = crawler.settings.get("PAGE_LIMIT", 0)
        return cls(page_limit)

    def process_request(self, request, spider):
        logger.debug(f"Processing request {request}")
        if self.current_page_count >= self.page_limit:
            raise IgnoreRequest(f"Page limit reached. Ignoring request {request}")

    def process_response(self, request, response, spider):
        logger.debug(f"Processing request {request} response")
        if response.status == 200:
            self.current_page_count += 1
        return response


class CustomHeadersMiddleware(DefaultHeadersMiddleware):
    @classmethod
    def from_crawler(cls, crawler):
        headers = without_none_values(crawler.settings["DEFAULT_REQUEST_HEADERS"])
        if custom_header := without_none_values(crawler.settings.get("CUSTOM_HEADERS")):
            headers.update(custom_header)
        return cls(headers.items())


class HtmlStorageMiddleware:
    def __init__(self, page_limit: int):
        self.page_limit = page_limit
        self.current_page_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        page_limit = crawler.settings.get("CLOSESPIDER_PAGECOUNT", 0)
        return cls(page_limit)

    def process_response(self, request, response, spider):
        if self.current_page_count >= self.page_limit:
            raise IgnoreRequest(f"Page limit reached. Ignoring request {request}")
        logger.debug(f"Processing request {request} response")
        if response.status == 200:
            self.current_page_count += 1
            logger.info(f"Storing response html.")
        return response
