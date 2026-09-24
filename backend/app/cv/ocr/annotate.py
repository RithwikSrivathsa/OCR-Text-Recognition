from datetime import datetime
from pathlib import Path

import cv2

from app.cv.types import BoundingBox, Frame, OcrResult


def draw_annotation(
    frame: Frame,
    tanker_bbox: BoundingBox,
    track_id: str,
    ocr_result: OcrResult | None,
    text_en: str,
    camera_id: str,
    timestamp: datetime,
    output_path: Path,
) -> Path:
    annotated = frame.copy()
    cv2.rectangle(annotated, (tanker_bbox.x1, tanker_bbox.y1), (tanker_bbox.x2, tanker_bbox.y2), (0, 255, 0), 2)
    cv2.putText(annotated, track_id, (tanker_bbox.x1, max(24, tanker_bbox.y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    if ocr_result:
        pts = [(int(x), int(y)) for x, y in ocr_result.polygon]
        for idx, start in enumerate(pts):
            end = pts[(idx + 1) % len(pts)]
            cv2.line(annotated, start, end, (255, 180, 0), 2)
        label = f"OCR {ocr_result.confidence:.2f}: {ocr_result.text_kn} | {text_en}"
        cv2.putText(annotated, label[:90], (tanker_bbox.x1, tanker_bbox.y2 + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 180, 0), 2)

    footer = f"{timestamp.isoformat(timespec='seconds')} {camera_id}"
    cv2.putText(annotated, footer, (16, annotated.shape[0] - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), annotated)
    return output_path

