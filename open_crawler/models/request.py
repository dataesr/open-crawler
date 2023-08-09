from typing import Any, Optional

from pydantic import BaseModel

from models.crawl import MetadataConfig, CrawlConfig, CrawlParameters
from models.enums import MetadataType
from services.url_cleaner import clean_url


class MetadataRequest(BaseModel):
    name: MetadataType
    enabled: Optional[bool] = None
    depth: Optional[int] = None


class CrawlRequest(BaseModel):
    url: str
    depth: Optional[int] = None
    limit: Optional[int] = None
    headers: dict[str, Any] = {}
    metadata: list[MetadataRequest] = []
    tags: list[str] = []

    def to_config(self) -> CrawlConfig:
        config = CrawlConfig(
            url=clean_url(self.url),
            parameters=CrawlParameters(depth=self.depth, limit=self.limit),
            headers=self.headers,
            tags=self.tags,
        )
        for meta in self.metadata:
            config.metadata_config[MetadataType(meta.name)].update(meta.enabled, meta.depth)
        return config
