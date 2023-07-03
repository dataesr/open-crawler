from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from open_crawler.celery_broker.utils import create_celery_app
from open_crawler.config.config import settings
from open_crawler.crawler.spiders.demo_spider import DemoSpider

celery_app = create_celery_app()


@celery_app.task(queue=settings.RABBITMQ_QUEUE_NAME)
def get_crawl_task(url: str):
    # Use logs in real task
    print("Get crawl task with url" + url)
    # FIXME, project settings not good
    crawler_settings = get_project_settings()
    process = CrawlerProcess(crawler_settings)
    items = process.crawl(DemoSpider, start_urls=[url])
    process.start()
    for item in items:
        print(item)
