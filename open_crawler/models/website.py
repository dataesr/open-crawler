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
    next_crawl_at: datetime
    last_crawl: Optional[dict[str, Any]] = None

    def to_config(self) -> CrawlConfig:
        return CrawlConfig(
            url=self.url,
            parameters={"depth": self.depth, "limit": self.limit},
            headers=self.headers,
            tags=self.tags,
            enabled_metadata=[
                MetadataType.ACCESSIBILITY if self.accessibility.enabled else None,
                MetadataType.TECHNOLOGIES if self.technologies_and_trackers.enabled else None,
                MetadataType.RESPONSIVENESS if self.responsiveness.enabled else None,
                MetadataType.GOOD_PRACTICES if self.good_practices.enabled else None,
                MetadataType.CARBON_FOOTPRINT if self.carbon_footprint.enabled else None,
            ],
        )


class UpdateWebsiteModel(BaseModel):
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


class CreateWebsiteModel(BaseModel):
    url: str
    depth: Optional[int] = Field(ge=0, default=2)
    limit: Optional[int] = Field(ge=0, default=400)
    accessibility: Optional[MetadataConfig] = Field(default=MetadataConfig())
    technologies_and_trackers: Optional[MetadataConfig] = Field(
        default=MetadataConfig(enabled=False))
    responsiveness: Optional[MetadataConfig] = Field(
        default=MetadataConfig(enabled=False))
    good_practices: Optional[MetadataConfig] = Field(
        default=MetadataConfig(enabled=False))
    carbon_footprint: Optional[MetadataConfig] = Field(
        default=MetadataConfig(enabled=False))
    headers: Optional[dict[str, Any]] = Field(default={})
    tags: Optional[list[str]] = Field(default=[])
    crawl_every: Optional[int] = Field(ge=0, default=30)

    def to_website_model(self) -> WebsiteModel:
        website = self.model_dump()
        website["next_crawl_at"] = datetime.now(
        ) + timedelta(days=website["crawl_every"])
        website["created_at"] = datetime.now()
        website["updated_at"] = datetime.now()
        if not self.accessibility:
            website["accessibility"] = MetadataConfig()
        if not self.technologies_and_trackers:
            website["technologies_and_trackers"] = MetadataConfig()
        if not self.responsiveness:
            website["responsiveness"] = MetadataConfig()
        if not self.good_practices:
            website["good_practices"] = MetadataConfig()
        if not self.carbon_footprint:
            website["carbon_footprint"] = MetadataConfig()

        return WebsiteModel(**website)
