import os
from datetime import datetime

from pymongo.results import InsertOneResult

from models.crawl import CrawlProcess
from models.enums import MetadataType

from mongo import db


class CrawlsRepository():
    """Operations for crawls collection"""

    def __init__(self):
        self.collection = db[os.environ["MONGO_CRAWLS_COLLECTION"]]

    def create(self, data: CrawlProcess) -> str:
        result: InsertOneResult = self.collection.insert_one(data.model_dump())
        assert result.acknowledged
        return data.id

    def list(self, website_id, skip: int = 0, limit: int = 20) -> list[CrawlProcess]:
        filters = {}
        if website_id:
            filters["website_id"] = website_id
        cursor = self.collection.find(filters).skip(skip).limit(limit)
        return [CrawlProcess(**crawl) for crawl in cursor]

    def update_status(self, data: CrawlProcess):
        self.collection.update_one(
            filter={"id": data.id},
            update={
                "$set": {"status": data.status, "updated_at": datetime.now()}
            },
        )

    def update_metadata(self, data: CrawlProcess, metadata: MetadataType):
        self.collection.update_one(
            filter={"id": data.id},
            update={
                "$set": {
                    f"metadata.{metadata}": {
                        "status": data.metadata[metadata].status,
                        "updated_at": datetime.now(),
                    }
                }
            },
        )


crawls = CrawlsRepository()
