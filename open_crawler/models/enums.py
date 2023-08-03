from enum import StrEnum


class MetadataType(StrEnum):
    ACCESSIBILITY = "accessibility"
    TECHNOLOGIES = "technologies_and_trackers"
    RESPONSIVENESS = "responsiveness"
    GOOD_PRACTICES = "good_practices"
    CARBON_FOOTPRINT = "carbon_footprint"


class ProcessStatus(StrEnum):
    PENDING = "pending"
    STARTED = "started"
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL_ERROR = "partial_error"
