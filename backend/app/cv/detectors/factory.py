from app.core.config import settings
from app.cv.detectors.base import BaseVehicleDetector
from app.cv.detectors.generic import CustomTankerDetector, GenericTruckDetector


def create_detector() -> BaseVehicleDetector:
    if settings.detector_type == "custom_tanker":
        return CustomTankerDetector(settings.detector_model_path)
    return GenericTruckDetector(settings.detector_model_path)

