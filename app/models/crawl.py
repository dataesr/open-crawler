from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import MetadataType, ProcessStatus
from app.models.utils import get_uuid


class BaseTaskModel(BaseModel):
    task_id: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    status: ProcessStatus | None = None
    enabled: bool = Field(default=True)

    def update(
        self, status: ProcessStatus | None = None, task_id: str | None = None
    ):
        if task_id is not None:
            self.task_id = task_id
        if status is None:
            return
        if status == ProcessStatus.STARTED:
            self.started_at = datetime.utcnow()
        if status in [ProcessStatus.SUCCESS, ProcessStatus.ERROR]:
            self.finished_at = datetime.utcnow()
        self.status = status


class HTMLCrawlModel(BaseTaskModel):
    use_playwright: bool = Field(default=False)
    depth: int | None = Field(default=0, ge=0)
    limit: int | None = Field(default=400, ge=0)
    urls: list[str] | None = []
    headers: dict[str, str] | None = None
    redirection: str | None = None


class LighthouseModel(BaseTaskModel):
    score: float | None = None
    limit: int | None = Field(default=0, ge=0)


class TechnologiesAndTrackersModel(BaseTaskModel):
    technologies: list[str] | None = None
    trackers: list[str] | None = None
    limit: int | None = Field(default=0, ge=0)


class CarbonFootprintModel(BaseTaskModel):
    co2_emission: float | None = None
    limit: int | None = Field(default=0, ge=0)


class CrawlModel(BaseModel):
    id: str = Field(default_factory=get_uuid)
    website_id: str
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    finished_at: datetime | None = None
    status: ProcessStatus = ProcessStatus.PENDING
    html_crawl: HTMLCrawlModel = Field(default_factory=HTMLCrawlModel)
    lighthouse: LighthouseModel | None = Field(default_factory=LighthouseModel)
    technologies_and_trackers: TechnologiesAndTrackersModel | None = Field(
        default_factory=TechnologiesAndTrackersModel)
    carbon_footprint: CarbonFootprintModel | None = Field(
        default_factory=CarbonFootprintModel)

    @property
    def enabled_metadata(self) -> list[MetadataType]:
        res = []
        if self.lighthouse and self.lighthouse.enabled:
            res.append(MetadataType.LIGHTHOUSE)
        if self.technologies_and_trackers and self.technologies_and_trackers.enabled:
            res.append(MetadataType.TECHNOLOGIES)
        if self.carbon_footprint and self.carbon_footprint.enabled:
            res.append(MetadataType.CARBON_FOOTPRINT)
        return res

    def update_task(
        self,
        task: str,
        status: ProcessStatus | None = None,
        task_id: str | None = None,
    ):
        getattr(self, task).update(status, task_id)
        return self


class ListCrawlResponse(BaseModel):
    count: int
    data: list[CrawlModel]
