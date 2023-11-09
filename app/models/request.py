from datetime import datetime, timedelta
from typing import Any

from pydantic import BaseModel, Field

from app.models.metadata import MetadataConfig
from app.models.website import WebsiteModel
from app.services.url_cleaner import clean_url


class UpdateWebsiteRequest(BaseModel):
    depth: int | None = None
    limit: int | None = None
    lighthouse: MetadataConfig | None = None
    technologies_and_trackers: MetadataConfig | None = None
    responsiveness: MetadataConfig | None = None
    carbon_footprint: MetadataConfig | None = None
    headers: dict[str, Any] | None = None
    tags: list[str] | None = None
    crawl_every: int | None = Field(ge=0, default=None)
    next_crawl_at: datetime | None = None


class CreateWebsiteRequest(BaseModel):
    url: str
    depth: int = Field(ge=0, default=2)
    limit: int = Field(ge=0, default=400)
    lighthouse: MetadataConfig = Field(default=MetadataConfig())
    technologies_and_trackers: MetadataConfig = Field(
        default=MetadataConfig(enabled=False)
    )
    responsiveness: MetadataConfig = Field(
        default=MetadataConfig(enabled=False)
    )
    carbon_footprint: MetadataConfig = Field(
        default=MetadataConfig(enabled=False)
    )
    headers: dict[str, Any] = Field(default={})
    tags: list[str] = Field(default=[])
    crawl_every: int = Field(ge=0, default=30)

    def to_website_model(self) -> WebsiteModel:
        self.url = clean_url(self.url)
        website = WebsiteModel(**self.model_dump())
        website.refresh_next_crawl_date()

        return website
