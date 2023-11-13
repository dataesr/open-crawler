from typing import Optional

from pydantic import BaseModel, Field

from app.models.utils import BaseTaskModel


class MetadataConfig(BaseModel):
    enabled: Optional[bool] = Field(default=True)
    depth: Optional[int] = Field(ge=0, default=0)


class MetadataTask(BaseTaskModel):
    pass


class LighthouseModel(MetadataTask):
    score: float | None = None
