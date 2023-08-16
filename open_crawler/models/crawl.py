from datetime import datetime
from typing import Optional, Any, Self

from pydantic import BaseModel, Field

from models.enums import MetadataType, ProcessStatus


class MetadataConfig(BaseModel):
    enabled: bool
    depth: int

    def update(self, enabled: Optional[bool] = None, depth: Optional[int] = None):
        if enabled is not None:
            self.enabled = enabled
        if depth is not None:
            self.depth = depth
            if enabled is None:
                self.enabled = True


class CrawlParameters(BaseModel):
    depth: Optional[int]
    limit: Optional[int]


DEFAULT_METADATA_CONFIG: dict[MetadataType, MetadataConfig] = {
    MetadataType.ACCESSIBILITY: MetadataConfig(enabled=True, depth=0),
    MetadataType.TECHNOLOGIES: MetadataConfig(enabled=False, depth=0),
    MetadataType.GOOD_PRACTICES: MetadataConfig(enabled=False, depth=0),
    MetadataType.RESPONSIVENESS: MetadataConfig(enabled=False, depth=0),
    MetadataType.CARBON_FOOTPRINT: MetadataConfig(enabled=False, depth=0),
}


class CrawlConfig(BaseModel):
    url: str
    parameters: CrawlParameters
    metadata_config: dict[MetadataType, MetadataConfig] = DEFAULT_METADATA_CONFIG
    headers: Optional[dict[str, Any]]
    tags: list[str]


class MetadataProcess(BaseModel):
    urls: list[str] = []
    status: ProcessStatus = ProcessStatus.PENDING
    to_save: bool = True

    def set_status(self, status: ProcessStatus):
        if self.status != status:
            self.status = status
            self.to_save = True


class CrawlProcess(BaseModel):
    config: CrawlConfig = None
    date: datetime = Field(default_factory=datetime.now)
    status: ProcessStatus = ProcessStatus.PENDING
    id: str = ""
    metadata: dict[MetadataType, MetadataProcess] = {}
    base_file_path: str = ""

    @property
    def enabled_metadata(self) -> list[MetadataType]:
        return [meta_type for meta_type, meta_config in self.config.metadata_config.items() if meta_config.enabled]

    def save_url_for_metadata(self, url: str, depth: int):
        for meta in self.enabled_metadata:
            if depth <= self.config.metadata_config[meta].depth:
                self.metadata.setdefault(meta, MetadataProcess()).urls.append(url)

    def set_from(self, other: Self):
        self.config = other.config
        self.date = other.date
        self.status = other.status
        self.id = other.id
        self.metadata = other.metadata

    def set_metadata_status(self, meta: MetadataType, status: ProcessStatus):
        self.metadata.get(meta).set_status(status)

    def metadata_needs_save(self, meta: MetadataType):
        return self.metadata.get(meta).to_save
