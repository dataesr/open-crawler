from datetime import datetime, timedelta
from typing import Optional, Any

from pydantic import BaseModel, Field

from app.models.crawl import CrawlModel
from app.models.utils import get_uuid, clean_url, is_domain


class MetadataConfig(BaseModel):
    enabled: bool | None = False
    depth: int | None = Field(ge=0, default=0)


class WebsiteModel(BaseModel):
    id: str = Field(default_factory=get_uuid)
    url: str
    depth: int
    limit: int
    use_playwright: bool
    lighthouse: MetadataConfig
    technologies_and_trackers: MetadataConfig
    carbon_footprint: MetadataConfig
    headers: dict[str, Any] | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tags: list[str]
    identifiers: list[str]
    crawl_every: int
    next_crawl_at: Optional[datetime] = None
    last_crawl: Optional[dict[str, Any]] = Field(None, examples=[{
        "id": "string",
        "website_id": "string",
        "config": {
            "url": "website_url",
            "parameters": {
                "depth": 2,
                "limit": 2,
                "use_playwright": False
            },
            "metadata_config": {
                "lighthouse": {
                    "enabled": True,
                    "depth": 0
                },
                "technologies_and_trackers": {
                    "enabled": True,
                    "depth": 0
                },
                "carbon_footprint": {
                    "enabled": True,
                    "depth": 0
                }
            },
            "headers": {},
            "tags": []
        },
        "created_at": "2023-12-01T07:53:38.330000",
        "started_at": "2023-12-01T07:53:38.493000",
        "finished_at": "2023-12-01T07:54:01.324000",
        "status": "success",
        "html_crawl": {
            "task_id": "task_id_html",
            "started_at": "2023-12-01T07:53:38.512000",
            "finished_at": "2023-12-01T07:53:40.829000",
            "status": "success"
        },
        "lighthouse": {
            "task_id": "task_id_lighthouse",
            "started_at": "2023-12-01T07:53:40.848000",
            "finished_at": "2023-12-01T07:54:01.295000",
            "status": "success",
            "score": 98
        },
        "technologies_and_trackers": {
            "task_id": "task_id_technologies_and_trackers",
            "started_at": "2023-12-01T07:53:40.850000",
            "finished_at": "2023-12-01T07:53:50.030000",
            "status": "success"
        },
        "carbon_footprint": {
            "task_id": "task_id_carbon_footprint",
            "started_at": "2023-12-01T07:53:40.853000",
            "finished_at": "2023-12-01T07:53:41.044000",
            "status": "success"
        }
    }])

    def to_crawl(self) -> CrawlModel:
        return CrawlModel(
            html_crawl={
                "use_playwright": self.use_playwright,
                "depth": self.depth,
                "limit": self.limit,
                "headers": self.headers,
            },
            website_id=self.id,
            url=self.url,
            lighthouse=self.lighthouse.model_dump(),
            technologies_and_trackers=self.technologies_and_trackers.model_dump(),
            carbon_footprint=self.carbon_footprint.model_dump(),
        )

    def refresh_next_crawl_date(self):
        self.next_crawl_at = (
            datetime.utcnow() + timedelta(days=self.crawl_every)
        ).replace(hour=0, minute=0, second=0)


class UpdateWebsiteRequest(BaseModel):
    depth: int | None = None
    limit: int | None = None
    use_playwright: bool = False
    lighthouse: MetadataConfig | None = None
    technologies_and_trackers: MetadataConfig | None = None
    carbon_footprint: MetadataConfig | None = None
    headers: dict[str, Any] | None = None
    tags: list[str] | None = None
    identifiers: list[str] | None = None
    crawl_every: int | None = Field(ge=0, default=None)
    next_crawl_at: datetime | None = None


class CreateWebsiteRequest(BaseModel):
    url: str
    depth: int = Field(ge=0, default=2)
    limit: int = Field(ge=0, default=400)
    use_playwright: bool = Field(default=False)
    lighthouse: MetadataConfig = Field(default=MetadataConfig())
    technologies_and_trackers: MetadataConfig = Field(
        default=MetadataConfig(enabled=False)
    )
    carbon_footprint: MetadataConfig = Field(
        default=MetadataConfig(enabled=False)
    )
    headers: dict[str, Any] = Field(default={})
    tags: list[str] = Field(default=[])
    identifiers: list[str] = Field(default=[])
    crawl_every: int = Field(ge=0, default=30)

    def to_website_model(self) -> WebsiteModel:
        self.url = clean_url(self.url)
        if not is_domain(self.url):
            self.depth = 0
            self.limit = 1
        website = WebsiteModel(**self.model_dump())
        website.refresh_next_crawl_date()

        return website


class ListWebsiteResponse(BaseModel):
    count: int
    data: list[WebsiteModel]
    tags: list[str]
    status: list[str]
