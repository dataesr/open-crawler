from datetime import datetime
from typing import Optional, Any, Self

from pydantic import BaseModel, Field

from models.enums import MetadataType, ProcessStatus
from models.utils import get_uuid


class MetadataConfig(BaseModel):
    enabled: bool
    depth: int

    def update(
        self, enabled: Optional[bool] = None, depth: Optional[int] = None
    ):
        if enabled is not None:
            self.enabled = enabled
        if depth is not None:
            self.depth = depth
            if enabled is None:
                self.enabled = True


class CrawlParameters(BaseModel):
    depth: Optional[int]
    limit: Optional[int]


class CrawlConfig(BaseModel):
    url: str
    parameters: CrawlParameters
    metadata_config: dict[MetadataType, MetadataConfig]
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
    id: str = Field(default_factory=get_uuid)
    website_id: str
    config: CrawlConfig = None
    created_at: datetime = Field(default_factory=datetime.now)
    status: ProcessStatus = ProcessStatus.PENDING
    metadata: dict[MetadataType, MetadataProcess] = {}
    base_file_path: str = ""

    @property
    def enabled_metadata(self) -> list[MetadataType]:
        return [
            meta_type
            for meta_type, meta_config in self.config.metadata_config.items()
            if meta_config.enabled
        ]

    def save_url_for_metadata(self, url: str, depth: int):
        for meta in self.enabled_metadata:
            if depth <= self.config.metadata_config[meta].depth:
                self.metadata.setdefault(meta, MetadataProcess()).urls.append(
                    url
                )

    def set_from(self, other: Self):
        self.config = other.config
        self.status = other.status
        self.id = other.id
        self.metadata = other.metadata

    def set_metadata_status(self, meta: MetadataType, status: ProcessStatus):
        self.metadata.get(meta).set_status(status)

    def metadata_needs_save(self, meta: MetadataType):
        return self.metadata.get(meta).to_save
