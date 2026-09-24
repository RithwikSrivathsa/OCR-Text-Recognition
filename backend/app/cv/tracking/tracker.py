from datetime import datetime, timedelta

from app.core.config import settings
from app.cv.types import Detection, Track


class SimpleIoUTracker:
    """Small restart-safe interface placeholder for ByteTrack/BoT-SORT.

    This keeps pipeline contracts testable until a production tracker package is
    selected and licensed for the deployment.
    """

    def __init__(self):
        self._tracks: dict[str, Track] = {}
        self._next_id = 1

    def update(self, detections: list[Detection], now: datetime) -> list[Track]:
        matched: set[str] = set()
        for detection in detections:
            track_id = self._match(detection)
            if track_id is None:
                track_id = f"TANKER-{self._next_id}"
                self._next_id += 1
                self._tracks[track_id] = Track(
                    track_id=track_id,
                    bbox=detection.bbox,
                    confidence=detection.confidence,
                    first_seen_at=now,
                    last_seen_at=now,
                )
            else:
                track = self._tracks[track_id]
                track.bbox = detection.bbox
                track.confidence = detection.confidence
                track.last_seen_at = now
            matched.add(track_id)

        timeout = timedelta(seconds=settings.track_timeout_seconds)
        self._tracks = {
            track_id: track for track_id, track in self._tracks.items()
            if now - track.last_seen_at <= timeout
        }
        return list(self._tracks.values())

    def _match(self, detection: Detection) -> str | None:
        best_id = None
        best_iou = 0.0
        for track_id, track in self._tracks.items():
            iou = _iou(track.bbox.as_list(), detection.bbox.as_list())
            if iou > best_iou:
                best_iou = iou
                best_id = track_id
        return best_id if best_iou >= 0.25 else None


def _iou(a: list[int], b: list[int]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)
    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
    a_area = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    b_area = max(0, bx2 - bx1) * max(0, by2 - by1)
    union = a_area + b_area - inter_area
    return inter_area / union if union else 0.0

