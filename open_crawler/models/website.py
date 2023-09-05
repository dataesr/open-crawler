import os
from datetime import datetime, timedelta
from typing import Optional, Any
from pydantic import BaseModel, Field
from models.enums import MetadataType
from models.crawl import CrawlConfig
from .utils import get_uuid

DEFAULT_RECRAWL_INTERVAL = os.environ.get("DEFAULT_RECRAWL_INTERVAL", 30)


class MetadataConfig(BaseModel):
    enabled: Optional[bool] = Field(default=True)
    depth: Optional[int] = Field(ge=0, default=0)


class WebsiteModel(BaseModel):
    id: str = Field(default_factory=get_uuid)
    url: str
    depth: int
    limit: int
    accessibility: MetadataConfig
    technologies_and_trackers: MetadataConfig
    responsiveness: MetadataConfig
    good_practices: MetadataConfig
    carbon_footprint: MetadataConfig
    headers: dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    tags: list[str]
    crawl_every: int
    next_crawl_at: Optional[datetime] = None
    last_crawl: Optional[dict[str, Any]] = None

    def to_config(self) -> CrawlConfig:
        return CrawlConfig(
            url=self.url,
            parameters={"depth": self.depth, "limit": self.limit},
            headers=self.headers,
            tags=self.tags,
            metadata_config={
                MetadataType.ACCESSIBILITY: self.accessibility.model_dump(),
                MetadataType.TECHNOLOGIES: self.technologies_and_trackers.model_dump(),
                MetadataType.RESPONSIVENESS: self.responsiveness.model_dump(),
                MetadataType.GOOD_PRACTICES: self.good_practices.model_dump(),
                MetadataType.CARBON_FOOTPRINT: self.carbon_footprint.model_dump(),
            },
        )


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
