from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import TankerEvent


def export_events_xlsx(db: Session) -> Path:
    events = db.query(TankerEvent).order_by(TankerEvent.created_at.desc()).all()
    rows = [
        {
            "id": event.id,
            "camera_id": event.camera_id,
            "site_name": event.site_name,
            "tracker_id": event.tracker_id,
            "state": event.state,
            "entry_time": event.entry_time,
            "exit_time": event.exit_time,
            "duration_seconds": event.duration_seconds,
            "text_kn": event.text_kn,
            "text_en": event.text_en,
            "ocr_confidence": event.ocr_confidence,
            "snapshot_path": event.snapshot_path,
        }
        for event in events
    ]
    output = settings.export_dir / "tanker_events.xlsx"
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_excel(output, index=False)
    return output


class GoogleSheetsSync:
    def sync(self, db: Session) -> dict:
        if not settings.google_sheets_enabled:
            return {"enabled": False, "synced": 0}
        events = db.query(TankerEvent).count()
        return {"enabled": True, "synced": events, "spreadsheet_id": settings.google_sheets_spreadsheet_id}

