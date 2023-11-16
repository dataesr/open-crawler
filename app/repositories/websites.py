import os
from typing import Any

from pymongo.results import InsertOneResult, UpdateResult

from app.celery_broker.utils import french_datetime
from app.config import settings
from app.models.enums import ProcessStatus
from app.models.request import UpdateWebsiteRequest
from app.models.website import WebsiteModel, ListWebsiteResponse
from app.mongo import db


class WebsitesRepository:
    """Operations for websites collection"""

    def __init__(self):
        self.collection = db[settings.MONGO_WEBSITES_COLLECTION]

    def list(
        self,
        query: str | None,
        tags: str | None,
        status: str | None,
        skip: int = 0,
        limit: int = 20,
        sort: str = "created_at",
    ) -> ListWebsiteResponse:
        filters = {}
        if query:
            filters["url"] = {"$regex": query}
        if tags:
            filters["tags"] = {"$elemMatch": {"$in": tags.split(",")}}
        if status:
            filters["last_crawl.status"] = {"$in": status.split(",")}
        if sort[0] == "-":
            sorter = [(sort[1:], -1)]
        else:
            sorter = [(sort, 1)]
        cursor = (
            self.collection.find(filters).skip(skip).limit(limit).sort(sorter)
        )
        data = [WebsiteModel(**website) for website in cursor]
        count = self.collection.count_documents(filters)
        tags = self.collection.distinct("tags")
        statuses = self.collection.distinct("last_crawl.status")
        return ListWebsiteResponse(
            data=data,
            count=count,
            tags=tags,
            status=[ProcessStatus(status) for status in statuses],
        )

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
        assert result.matched_count == 1

    def delete(self, website_id: str) -> None:
        self.collection.delete_one({"id": website_id})

    def store_last_crawl(self, website_id: str, crawl: dict[str, Any]):
        result: UpdateResult = self.collection.update_one(
            filter={"id": website_id}, update={"$set": {"last_crawl": crawl}}
        )
        assert result.modified_count == 1

    def refresh_next_crawl(self, website_id: str):
        website = self.get(website_id=website_id)
        website.refresh_next_crawl_date()
        self.update(
            website_id=website_id,
            data=UpdateWebsiteRequest(next_crawl_at=website.next_crawl_at),
        )

    def list_to_recrawl(self) -> ListWebsiteResponse:
        filters = {"next_crawl_at": {"$lte": french_datetime()}}

        cursor = self.collection.find(filters)
        data = [WebsiteModel(**website) for website in cursor]
        count = self.collection.count_documents(filters)
        tags = self.collection.distinct("tags")
        statuses = self.collection.distinct("last_crawl.status")
        return ListWebsiteResponse(
            data=data,
            count=count,
            tags=tags,
            status=[ProcessStatus(status) for status in statuses],
        )


websites = WebsitesRepository()
