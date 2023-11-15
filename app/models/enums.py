from strenum import StrEnum


class MetadataType(StrEnum):
    LIGHTHOUSE = "lighthouse"
    TECHNOLOGIES = "technologies_and_trackers"
    RESPONSIVENESS = "responsiveness"
    CARBON_FOOTPRINT = "carbon_footprint"


class ProcessStatus(StrEnum):
    PENDING = "pending"
    STARTED = "started"
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL_ERROR = "partial_error"
