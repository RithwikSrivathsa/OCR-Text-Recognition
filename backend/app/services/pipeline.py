import asyncio
import json
from datetime import datetime

import structlog

from app.core.config import settings
from app.cv.detectors.factory import create_detector
from app.cv.ocr.annotate import draw_annotation
from app.cv.ocr.processor import KannadaOcrProcessor
from app.cv.tracking.tracker import SimpleIoUTracker
from app.db.session import SessionLocal
from app.services.events import EventManager
from app.services.snapshot import SnapshotPolicy
from app.services.stream import RtspStreamManager
from app.services.translation import KannadaTranslator

log = structlog.get_logger()


class PipelineRuntime:
    def __init__(self):
        self.stream = RtspStreamManager()
        self.detector = create_detector()
        self.tracker = SimpleIoUTracker()
        self.events = EventManager()
        self.snapshots = SnapshotPolicy()
        self.ocr = KannadaOcrProcessor()
        self.translator = KannadaTranslator()
        self.active_tracks = {}
        self._task: asyncio.Task | None = None
        self._last_centers: dict[str, tuple[float, float]] = {}

    async def start(self) -> None:
        self._task = asyncio.create_task(self._run(), name="pipeline-runtime")

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        await self.stream.stop()

    def status(self) -> dict:
        return {
            "camera": {
                "camera_id": settings.camera_id,
                "camera_name": settings.camera_name,
                "site_name": settings.site_name,
                "connected": self.stream.health.connected,
                "last_frame_at": self.stream.health.last_frame_at,
                "last_error": self.stream.health.last_error,
            },
            "active_tankers": [
                {
                    "track_id": track.track_id,
                    "bbox": track.bbox.as_list(),
                    "confidence": track.confidence,
                    "first_seen_at": track.first_seen_at,
                    "last_seen_at": track.last_seen_at,
                    "stationary_since": track.stationary_since,
                }
                for track in self.active_tracks.values()
            ],
            "updated_at": datetime.utcnow(),
        }

    async def _run(self) -> None:
        frame_delay = 1 / max(settings.detection_fps, 0.1)
        async for frame in self.stream.frames():
            if frame is None:
                await asyncio.sleep(frame_delay)
                continue
            now = datetime.utcnow()
            detections = self.detector.detect(frame)
            tracks = self.tracker.update(detections, now)
            self.active_tracks = {track.track_id: track for track in tracks}

            with SessionLocal() as db:
                for track in tracks:
                    previous = self._last_centers.get(track.track_id)
                    self.snapshots.update_stationary(track, previous, now)
                    self._last_centers[track.track_id] = track.bbox.center
                    event = self.events.update_track_present(db, track, now)

                    if self.snapshots.should_capture(track, now):
                        result = self.ocr.run(frame, track.bbox)
                        text_en = self.translator.translate(result.text_kn) if result else ""
                        path = self.snapshots.path_for(track.track_id, now)
                        draw_annotation(frame, track.bbox, track.track_id, result, text_en, settings.camera_id, now, path)
                        track.last_snapshot_at = now
                        event.snapshot_path = str(path)
                        if result:
                            event.text_kn = result.text_kn
                            event.text_en = text_en
                            event.ocr_confidence = result.confidence
                            event.ocr_polygon_json = json.dumps(result.polygon)
                            event.preprocessing_method = result.preprocessing_method
                            event.ocr_model_version = result.model_version
                        event.updated_at = now
                        db.commit()

                self.events.complete_missing_tracks(db, set(self.active_tracks), now)

            await asyncio.sleep(frame_delay)

