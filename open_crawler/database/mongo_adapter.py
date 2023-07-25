from datetime import datetime
from typing import Any

from pymongo import MongoClient
from pymongo.results import InsertOneResult

from models.crawl import CrawlConfig, CrawlProcess
from models.enums import ProcessStatus


class MongoAdapter:
    def __init__(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client.website_crawl
        self.crawl_collection = self.db.website_crawl
        self.params_collection = self.db.website_crawl_params

    def save_crawl_params(self, crawl_config: CrawlConfig):
        self.params_collection.replace_one(
            filter={"url": crawl_config.url},
            replacement=crawl_config.dict(),
            upsert=True,
        )

    def insert_crawl(self, crawl: CrawlProcess) -> Any:
        result: InsertOneResult = self.crawl_collection.insert_one(
            {
                "id": crawl.date.strftime("%Y-%m-%d_%H_%M_%S"),
                "url": crawl.config.url,
                "date": crawl.date.isoformat(timespec="seconds"),
                "processStatus": crawl.status,
            }
        )

        crawl.id = result.inserted_id

    def update_crawl(self, crawl: CrawlProcess):
        self.crawl_collection.update_one(filter={"_id": crawl.id}, update={"$set": {"processStatus": crawl.status}})

    def new_crawl(self, crawl: CrawlProcess) -> Any:
        self.save_crawl_params(crawl.config)
        self.insert_crawl(crawl)


mongo = MongoAdapter()
