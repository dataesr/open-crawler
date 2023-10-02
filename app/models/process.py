from typing import Self

from pydantic import BaseModel

from app.models.crawl import CrawlConfig, CrawlModel
from app.models.enums import ProcessStatus, MetadataType


class MetadataProcess(BaseModel):
    urls: list[str] = []
    status: ProcessStatus = ProcessStatus.PENDING
    to_save: bool = True

    def set_status(self, status: ProcessStatus):
        if self.status != status:
            self.status = status
            self.to_save = True


class CrawlProcess(BaseModel):
    id: str
    website_id: str
    config: CrawlConfig
    status: ProcessStatus = ProcessStatus.PENDING
    metadata: dict[MetadataType, MetadataProcess] = {}

    @classmethod
    def from_model(cls, model: CrawlModel) -> Self:
        return cls(
            id=model.id, website_id=model.website_id, config=model.config
        )

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
