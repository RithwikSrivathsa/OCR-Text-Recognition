from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

from app.core.config import settings
from app.cv.types import Track


class SnapshotPolicy:
    def should_capture(self, track: Track, now: datetime) -> bool:
        if track.stationary_since is None:
            track.stationary_since = now
            return False

        stationary_for = now - track.stationary_since
        enough_stationary_time = stationary_for >= timedelta(seconds=settings.stationary_time_seconds)
        if not enough_stationary_time:
            return False

        if track.last_snapshot_at is None:
            return True
        return now - track.last_snapshot_at >= timedelta(seconds=settings.ocr_interval_seconds)

    def update_stationary(self, track: Track, previous_center: tuple[float, float] | None, now: datetime) -> None:
        if previous_center is None:
            track.stationary_since = track.stationary_since or now
            return

        current = np.array(track.bbox.center)
        previous = np.array(previous_center)
        distance = float(np.linalg.norm(current - previous))
        if distance <= settings.stationary_distance_threshold_pixels:
            track.stationary_since = track.stationary_since or now
        else:
            track.stationary_since = None

    def path_for(self, track_id: str, now: datetime) -> Path:
        stamp = now.strftime("%Y%m%d_%H%M%S")
        return settings.snapshot_dir / f"{track_id}_{stamp}.jpg"

