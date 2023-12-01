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
    use_playwright: bool
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
                                                            "responsiveness": {
                                                              "enabled": False,
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
                                                        "responsiveness": None,
                                                        "carbon_footprint": {
                                                          "task_id": "task_id_carbon_footprint",
                                                          "started_at": "2023-12-01T07:53:40.853000",
                                                          "finished_at": "2023-12-01T07:53:41.044000",
                                                          "status": "success"
                                                        }
                                                      }])

    def to_config(self) -> CrawlConfig:
        return CrawlConfig(
            url=self.url,
            parameters=CrawlParameters(depth=self.depth, limit=self.limit, use_playwright=self.use_playwright),
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
