from typing import Optional

from pydantic import BaseModel, Field

from models.utils import BaseTaskModel


class MetadataConfig(BaseModel):
    enabled: Optional[bool] = Field(default=True)
    depth: Optional[int] = Field(ge=0, default=0)


class MetadataTask(BaseTaskModel):
    pass


class AccessibilityModel(MetadataTask):
    score: float | None = None
