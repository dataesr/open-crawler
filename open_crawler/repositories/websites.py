import os
from typing import Any

from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from models.website import WebsiteModel, ListWebsiteResponse
from models.request import UpdateWebsiteRequest
from mongo import db


class WebsitesRepository:
    """Operations for websites collection"""

    def __init__(self):
        self.collection = db[os.environ["MONGO_WEBSITES_COLLECTION"]]

    def list(
        self,
        query: str,
        tags: str,
        status: str,
        skip: int = 0,
        limit: int = 20,
        sort: str = 'created_at',
    ) -> ListWebsiteResponse:
        filters = {}
        if query:
            filters["url"] = {"$regex": query}
        if tags:
            filters["tags"] = {"$elemMatch": {"$in": tags.split(",")}}
        if status:
            filters["last_crawl.status"] = {"$in": status.split(",")}
        if (sort[0] == '-'):
            sorter = [(sort[1:], -1)]
        else:
            sorter = [(sort, 1)]
        cursor = self.collection.find(filters).skip(
            skip).limit(limit).sort(sorter)
        data = [website for website in cursor]
        count = self.collection.count_documents(filters)
        tags = self.collection.distinct("tags")
        status = self.collection.distinct("last_crawl.status")
        return {"data": data, "count": count, "tags": tags, "status": status}

    def create(self, data: WebsiteModel) -> str:
        result: InsertOneResult = self.collection.insert_one(data.model_dump())
        assert result.acknowledged
        return data.id

    def get(self, website_id: str) -> WebsiteModel:
        if data := self.collection.find_one({"id": website_id}):
            return WebsiteModel(**data)

    def update(self, website_id: str, data: UpdateWebsiteRequest) -> None:
        result: UpdateResult = self.collection.update_one(
            {"id": website_id}, {"$set": data.model_dump(exclude_unset=True)}
        )
        assert result.acknowledged

    def delete(self, website_id: str) -> None:
        result: DeleteResult = self.collection.delete_one({"id": website_id})
        assert result.acknowledged

    def store_last_crawl(self, website_id: str, crawl: dict[str, Any]):
        result: UpdateResult = self.collection.update_one(
            filter={"id": website_id}, update={"$set": {"last_crawl": crawl}}
        )
        assert result.acknowledged


websites = WebsitesRepository()
