from datetime import datetime
from uuid import uuid4

__all__ = "get_uuid"

from pydantic import BaseModel

from models.enums import ProcessStatus


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())


class BaseTaskModel(BaseModel):
    task_id: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    status: ProcessStatus = ProcessStatus.PENDING

    def update(
        self, status: ProcessStatus | None = None, task_id: str | None = None
    ):
        if task_id is not None:
            self.task_id = task_id
        if status is None:
            return
        if status == ProcessStatus.STARTED:
            self.started_at = datetime.now()
        if status == ProcessStatus.SUCCESS:
            self.finished_at = datetime.now()
        self.status = status
