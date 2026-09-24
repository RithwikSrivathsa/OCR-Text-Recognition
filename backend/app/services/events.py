import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.config import settings
from app.cv.types import Track
from app.db.models import EventState, TankerEvent


class EventManager:
    def __init__(self):
        self.active_event_ids: dict[str, int] = {}

    def update_track_present(self, db: Session, track: Track, now: datetime) -> TankerEvent:
        event = self._get_or_create(db, track, now)
        event.state = EventState.PRESENT.value
        event.updated_at = now
        event.tanker_bbox_json = json.dumps(track.bbox.as_list())
        db.commit()
        db.refresh(event)
        return event

    def complete_missing_tracks(self, db: Session, active_track_ids: set[str], now: datetime) -> None:
        for track_id, event_id in list(self.active_event_ids.items()):
            if track_id in active_track_ids:
                continue
            event = db.get(TankerEvent, event_id)
            if not event or event.exit_time:
                self.active_event_ids.pop(track_id, None)
                continue
            event.state = EventState.COMPLETED.value
            event.exit_time = now
            if event.entry_time:
                event.duration_seconds = (now - event.entry_time).total_seconds()
            event.updated_at = now
            self.active_event_ids.pop(track_id, None)
        db.commit()

    def _get_or_create(self, db: Session, track: Track, now: datetime) -> TankerEvent:
        event_id = self.active_event_ids.get(track.track_id)
        if event_id:
            event = db.get(TankerEvent, event_id)
            if event:
                return event

        event = TankerEvent(
            camera_id=settings.camera_id,
            site_name=settings.site_name,
            tracker_id=track.track_id,
            state=EventState.ENTERING.value,
            entry_time=now,
            tanker_bbox_json=json.dumps(track.bbox.as_list()),
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        self.active_event_ids[track.track_id] = event.id
        return event

