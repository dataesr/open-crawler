from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, ConfigDict

from models.enums import MetadataType, ProcessStatus


class ImmutableModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class MetaDataConfig(ImmutableModel):
    name: MetadataType
    enabled: bool
    depth: int


class CrawlParameters(ImmutableModel):
    depth: int
    limit: int


class CrawlConfig(ImmutableModel):
    url: str
    parameters: CrawlParameters
    metadata_config: Optional[list[MetaDataConfig]]
    headers: Optional[dict[str, Any]]


class CrawlProcess(BaseModel):
    config: CrawlConfig
    date: datetime = datetime.now()
    status: ProcessStatus = ProcessStatus.PENDING
    id: str = None
