from abc import ABC, abstractmethod

from app.cv.types import Detection, Frame


class BaseVehicleDetector(ABC):
    name = "base"

    @abstractmethod
    def detect(self, frame: Frame) -> list[Detection]:
        """Return tanker-like vehicle detections for a frame."""

