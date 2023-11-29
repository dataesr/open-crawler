from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.celery_broker.utils import french_datetime
from app.models.enums import MetadataType, ProcessStatus
from app.models.metadata import MetadataConfig, LighthouseModel, MetadataTask
from app.models.utils import get_uuid, BaseTaskModel


class CrawlParameters(BaseModel):
    depth: int
    limit: int
    use_playwright: bool


class CrawlConfig(BaseModel):
    url: str
    parameters: CrawlParameters
    metadata_config: dict[MetadataType, MetadataConfig] = Field(default_factory=dict, examples=[
                                                                                {
                                                                                    "lighthouse": {
                                                                                        "enabled": True,
                                                                                        "depth": 0
                                                                                    },
                                                                                    "technologies_and_trackers": {
                                                                                        "enabled": True,
                                                                                        "depth": 0
                                                                                    },
                                                                                    "responsiveness": {
                                                                                        "enabled": True,
                                                                                        "depth": 0
                                                                                    },
                                                                                    "carbon_footprint": {
                                                                                        "enabled": True,
                                                                                        "depth": 0
                                                                                    }
                                                                                }
                                                                            ])
    headers: dict[str, Any]
    tags: list[str]


class CrawlModel(BaseModel):
    id: str = Field(default_factory=get_uuid)
    website_id: str
    config: CrawlConfig
    created_at: datetime = Field(default_factory=french_datetime)
    started_at: datetime | None = None
    finished_at: datetime | None = None
    status: ProcessStatus = ProcessStatus.PENDING
    html_crawl: BaseTaskModel = Field(default_factory=BaseTaskModel)
    lighthouse: LighthouseModel | None = None
    technologies_and_trackers: MetadataTask | None = None
    responsiveness: MetadataTask | None = None
    carbon_footprint: MetadataTask | None = None

    @property
    def enabled_metadata(self) -> list[MetadataType]:
        return [
            meta_type
            for meta_type, meta_config in self.config.metadata_config.items()
            if meta_config.enabled
        ]

    def init_tasks(self) -> None:
        if MetadataType.LIGHTHOUSE in self.enabled_metadata:
            self.lighthouse = LighthouseModel()
        if MetadataType.TECHNOLOGIES in self.enabled_metadata:
            self.technologies_and_trackers = MetadataTask()
        if MetadataType.RESPONSIVENESS in self.enabled_metadata:
            self.responsiveness = MetadataTask()
        if MetadataType.CARBON_FOOTPRINT in self.enabled_metadata:
            self.carbon_footprint = MetadataTask()

    def update_task(
        self,
        task: str,
        status: ProcessStatus | None = None,
        task_id: str | None = None,
    ):
        getattr(self, task).update(status, task_id)

    def update_status(self, status: ProcessStatus):
        if status == ProcessStatus.STARTED:
            self.started_at = french_datetime()
        if status == ProcessStatus.SUCCESS:
            self.finished_at = french_datetime()
        self.status = status


class ListCrawlResponse(BaseModel):
    count: int
    data: list[CrawlModel]
