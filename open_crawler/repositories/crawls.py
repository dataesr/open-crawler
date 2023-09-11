import os
from datetime import datetime

from pymongo.results import InsertOneResult

from models.crawl import CrawlModel
from models.enums import ProcessStatus
from models.metadata import MetadataTask
from mongo import db


class CrawlsRepository:
    """Operations for crawls collection"""

    def __init__(self):
        self.collection = db[os.environ["MONGO_CRAWLS_COLLECTION"]]

    def create(self, data: CrawlModel) -> str:
        result: InsertOneResult = self.collection.insert_one(data.model_dump())
        assert result.acknowledged
        return data.id

    def list(
        self, website_id: str | None = None, skip: int = 0, limit: int = 20
    ) -> list[CrawlModel]:
        filters = {}
        if website_id:
            filters["website_id"] = website_id
        cursor = self.collection.find(filters).skip(skip).limit(limit)
        return [CrawlModel(**crawl) for crawl in cursor]

    def get(
        self, website_id: str | None = None, crawl_id: str | None = None
    ) -> CrawlModel:
        filters = {}
        if crawl_id:
            filters["id"] = crawl_id
        if website_id:
            filters["website_id"] = website_id
        crawl = self.collection.find_one(filters)
        return CrawlModel(**crawl)

    def update(self, data: CrawlModel):
        self.collection.update_one(
            filter={"id": data.id},
            update={"$set": data.model_dump(exclude_unset=True, exclude_defaults=True)},
        )

    def update_status(self, crawl_id: str, status: ProcessStatus):
        update_dict = {"status": status}
        if status == ProcessStatus.STARTED:
            update_dict["started_at"] = datetime.now()
        if status == ProcessStatus.SUCCESS:
            update_dict["finished_at"] = datetime.now()
        self.collection.update_one(
            filter={"id": crawl_id},
            update={"$set": update_dict},
        )

    def update_task(self, crawl_id: str, task_name: str, task: MetadataTask):
        self.collection.update_one(
            filter={"id": crawl_id},
            update={"$set": {task_name: task.model_dump()}},
        )


crawls = CrawlsRepository()
