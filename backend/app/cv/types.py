from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import numpy as np


@dataclass(frozen=True)
class BoundingBox:
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def center(self) -> tuple[float, float]:
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

    def as_list(self) -> list[int]:
        return [self.x1, self.y1, self.x2, self.y2]


@dataclass(frozen=True)
class Detection:
    bbox: BoundingBox
    confidence: float
    class_name: str


@dataclass
class Track:
    track_id: str
    bbox: BoundingBox
    confidence: float
    first_seen_at: datetime
    last_seen_at: datetime
    stationary_since: datetime | None = None
    last_snapshot_at: datetime | None = None
    metadata: dict = field(default_factory=dict)


class TrackLifecycle(str, Enum):
    NOT_PRESENT = "NOT_PRESENT"
    ENTERING = "ENTERING"
    PRESENT = "PRESENT"
    EXITING = "EXITING"
    COMPLETED = "COMPLETED"


@dataclass
class OcrResult:
    text_kn: str
    confidence: float
    polygon: list[list[int]]
    bbox: BoundingBox | None
    preprocessing_method: str
    model_version: str


Frame = np.ndarray

