import os
from datetime import datetime, timedelta
from typing import Optional, Any

from pydantic import BaseModel, Field

from models.crawl import CrawlConfig, CrawlParameters
from models.enums import MetadataType
from .metadata import MetadataConfig
from .utils import get_uuid

DEFAULT_RECRAWL_INTERVAL = os.environ.get("DEFAULT_RECRAWL_INTERVAL", 30)


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
            parameters=CrawlParameters(depth=self.depth, limit=self.limit),
            metadata_config={
                MetadataType.ACCESSIBILITY: self.accessibility,
                MetadataType.TECHNOLOGIES: self.technologies_and_trackers,
                MetadataType.RESPONSIVENESS: self.responsiveness,
                MetadataType.GOOD_PRACTICES: self.good_practices,
                MetadataType.CARBON_FOOTPRINT: self.carbon_footprint,
            },
            headers=self.headers,
            tags=self.tags,
        )

    def refresh_next_crawl_date(self):
        self.next_crawl_at = datetime.now() + timedelta(days=self.crawl_every)


class ListWebsiteResponse(BaseModel):
    count: int
    data: list[WebsiteModel]
    tags: list[str]
    status: list[str]
