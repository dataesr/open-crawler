# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
from open_crawler.config.config import settings


class CrawlerPipeline:
    def process_item(self, item, spider):
        return item


# Don't forget to declare the pipeline in the scrapy settings
class MongoDBPipeline:
    def __init__(self):
        print("MongoDBPipeline___init")

        mongodb_host = settings.get("MONGODB_HOST")
        mongodb_port = settings.get("MONGODB_PORT")
        mongodb_database = settings.get("MONGODB_DATABASE")
        mongodb_collection = settings.get("MONGODB_COLLECTION")

        self.client = MongoClient(mongodb_host, mongodb_port)
        self.db = self.client[mongodb_database]
        self.collection = self.db[mongodb_collection]

    def process_item(self, item, spider):
        print("saving_item_to_db")
        self.collection.insert_one(dict(item))
        return item