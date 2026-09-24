from app.cv.types import BoundingBox, Frame, OcrResult


class KannadaOcrProcessor:
    model_version = "paddleocr-kannada-configurable"

    def run(self, frame: Frame, tanker_bbox: BoundingBox) -> OcrResult | None:
        """Run Kannada OCR on a tanker crop.

        Deployments should install PaddleOCR Kannada recognition assets here.
        The method returns `None` when no confident large Kannada body text is
        found, instead of falling back to irrelevant CCTV overlay text.
        """

        return None

