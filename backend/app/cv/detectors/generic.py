import structlog

from app.core.config import settings
from app.cv.detectors.base import BaseVehicleDetector
from app.cv.types import Detection, Frame

log = structlog.get_logger()


class GenericTruckDetector(BaseVehicleDetector):
    """Adapter placeholder for a licensed detector runtime.

    Wire your chosen detector here, map detections into `Detection`, and keep
    the rest of the pipeline unchanged.
    """

    name = "generic_truck"

    def __init__(self, model_path: str | None = None):
        self.model_path = model_path or settings.detector_model_path
        log.info("detector.initialized", detector=self.name, model_path=self.model_path or "not_configured")

    def detect(self, frame: Frame) -> list[Detection]:
        return []


class CustomTankerDetector(GenericTruckDetector):
    name = "custom_tanker"

