from datetime import datetime, timedelta
from typing import Any

from pydantic import BaseModel, Field

from models.metadata import MetadataConfig
from models.website import WebsiteModel


class UpdateWebsiteRequest(BaseModel):
    depth: int | None = None
    limit: int | None = None
    accessibility: MetadataConfig | None = None
    technologies_and_trackers: MetadataConfig | None = None
    responsiveness: MetadataConfig | None = None
    good_practices: MetadataConfig | None = None
    carbon_footprint: MetadataConfig | None = None
    headers: dict[str, Any] | None = None
    tags: list[str] | None = None
    crawl_every: int | None = Field(ge=0, default=None)
    next_crawl_at: datetime | None = None


class CreateWebsiteRequest(BaseModel):
    url: str
    depth: int = Field(ge=0, default=2)
    limit: int = Field(ge=0, default=400)
    accessibility: MetadataConfig = Field(default=MetadataConfig())
    technologies_and_trackers: MetadataConfig = Field(
        default=MetadataConfig(enabled=False)
    )
    responsiveness: MetadataConfig = Field(
        default=MetadataConfig(enabled=False)
    )
    good_practices: MetadataConfig = Field(
        default=MetadataConfig(enabled=False)
    )
    carbon_footprint: MetadataConfig = Field(
        default=MetadataConfig(enabled=False)
    )
    headers: dict[str, Any] = Field(default={})
    tags: list[str] = Field(default=[])
    crawl_every: int = Field(ge=0, default=30)

    def to_website_model(self) -> WebsiteModel:
        website = WebsiteModel(**self.model_dump())
        website.next_crawl_at = datetime.now() + timedelta(
            days=self.crawl_every
        )

        return website
