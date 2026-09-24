from datetime import datetime

from app.cv.tracking.tracker import SimpleIoUTracker
from app.cv.types import BoundingBox, Detection


def test_tracker_keeps_id_for_overlapping_detection():
    tracker = SimpleIoUTracker()
    now = datetime.utcnow()
    first = tracker.update([Detection(BoundingBox(0, 0, 100, 100), 0.9, "tanker")], now)
    second = tracker.update([Detection(BoundingBox(5, 5, 105, 105), 0.9, "tanker")], now)

    assert first[0].track_id == second[0].track_id

