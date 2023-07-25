from typing import Any, Optional

from pydantic import BaseModel

from models.crawl import MetaDataConfig, CrawlConfig, CrawlParameters
from models.enums import MetadataType


class MetadataRequest(BaseModel):
    name: MetadataType
    enabled: bool
    depth: Optional[int] = 0

    def to_config(self) -> MetaDataConfig:
        return MetaDataConfig(name=self.name, enabled=self.enabled, depth=self.depth)


class CrawlRequest(BaseModel):
    url: str
    depth: int = None
    limit: int = None
    headers: dict[str, Any] = None
    metadata: list[MetadataRequest] = None

    def to_config(self) -> CrawlConfig:
        return CrawlConfig(
            url=self.url,
            parameters=CrawlParameters(depth=self.depth, limit=self.limit),
            headers=self.headers,
            metadata_config=[meta.to_config() for meta in self.metadata] if self.metadata else [],
        )
