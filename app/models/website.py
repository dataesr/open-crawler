import os
from datetime import datetime, timedelta
from typing import Optional, Any

from pydantic import BaseModel, Field

from app.celery_broker.utils import french_datetime
from app.models.crawl import CrawlConfig, CrawlParameters
from app.models.enums import MetadataType
from app.models.metadata import MetadataConfig
from app.models.utils import get_uuid



class WebsiteModel(BaseModel):
    id: str = Field(default_factory=get_uuid)
    url: str
    depth: int
    limit: int
    lighthouse: MetadataConfig
    technologies_and_trackers: MetadataConfig
    responsiveness: MetadataConfig
    carbon_footprint: MetadataConfig
    headers: dict[str, Any]
    created_at: datetime = Field(default_factory=french_datetime)
    updated_at: datetime = Field(default_factory=french_datetime)
    tags: list[str]
    crawl_every: int
    next_crawl_at: Optional[datetime] = None
    last_crawl: Optional[dict[str, Any]] = None

    def to_config(self) -> CrawlConfig:
        return CrawlConfig(
            url=self.url,
            parameters=CrawlParameters(depth=self.depth, limit=self.limit),
            metadata_config={
                MetadataType.LIGHTHOUSE: self.lighthouse,
                MetadataType.TECHNOLOGIES: self.technologies_and_trackers,
                MetadataType.RESPONSIVENESS: self.responsiveness,
                MetadataType.CARBON_FOOTPRINT: self.carbon_footprint,
            },
            headers=self.headers,
            tags=self.tags,
        )

    def refresh_next_crawl_date(self):
        self.next_crawl_at = (
            french_datetime() + timedelta(days=self.crawl_every)
        ).replace(hour=0, minute=0, second=0)


class ListWebsiteResponse(BaseModel):
    count: int
    data: list[WebsiteModel]
    tags: list[str]
    status: list[str]
