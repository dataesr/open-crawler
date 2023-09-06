import os
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from models.website import WebsiteModel, UpdateWebsiteRequest
from models.enums import ProcessStatus

from mongo import db


class WebsitesRepository:
    """Operations for websites collection"""

    def __init__(self):
        self.collection = db[os.environ["MONGO_WEBSITES_COLLECTION"]]

    def list(
        self,
        query: str,
        tags: list[str],
        status: list[ProcessStatus],
        skip: int = 0,
        limit: int = 20,
    ) -> list[WebsiteModel]:
        filters = {}
        if query is not None:
            filters["url"] = {"$regex": query}
        if tags is not None:
            filters["tags"] = {"$elemMatch": {"$in": tags}}
        if status is not None:
            filters["last_crawl.status"] = {{"$in": status}}
        cursor = self.collection.find(filters).skip(skip).limit(limit)
        return [WebsiteModel(**website) for website in cursor]

    def create(self, data: WebsiteModel) -> str:
        result: InsertOneResult = self.collection.insert_one(data.model_dump())
        assert result.acknowledged
        return data.id

    def get(self, id: str) -> WebsiteModel:
        data = self.collection.find_one({"id": id})
        if data:
            return WebsiteModel(**data)

    def update(self, id: str, data: UpdateWebsiteRequest) -> bool:
        result: UpdateResult = self.collection.update_one(
            {"id": id}, {"$set": data.model_dump(exclude_unset=True)}
        )
        assert result.acknowledged

    def delete(self, id: str) -> bool:
        result: DeleteResult = self.collection.delete_one({"id": id})
        assert result.acknowledged


websites = WebsitesRepository()
