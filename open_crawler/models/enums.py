from enum import StrEnum


class MetadataType(StrEnum):
    RGAA = "accessibility"
    TECHNOLOGIES = "technologies and trackers"
    RESPONSIVENESS = "responsiveness"
    GOODPRACTICES = "good practices"
    CARBON = "carbon footprint"


class ProcessStatus(StrEnum):
    PENDING = "pending"
    STARTED = "started"
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL_ERROR = "partial_error"
