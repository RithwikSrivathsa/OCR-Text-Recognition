import asyncio
import json
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.runtime import runtime
from app.core.security import mask_rtsp_url
from app.db.models import CameraConfig, TankerEvent
from app.db.session import get_db
from app.schemas.api import CameraConfigIn, CameraConfigOut, HealthOut, TankerEventOut
from app.services.exports import GoogleSheetsSync, export_events_xlsx

router = APIRouter()


@router.get("/health", response_model=HealthOut)
def health():
    status = runtime.status()
    return HealthOut(
        status="ok",
        camera_connected=status["camera"]["connected"],
        last_frame_at=status["camera"]["last_frame_at"],
        active_tracks=len(status["active_tankers"]),
    )


@router.get("/status")
def status():
    return runtime.status()


@router.get("/status/stream")
async def status_stream():
    async def events():
        while True:
            yield f"data: {json.dumps(runtime.status(), default=str)}\n\n"
            await asyncio.sleep(2)

    return StreamingResponse(events(), media_type="text/event-stream")


@router.get("/camera-config", response_model=CameraConfigOut)
def get_camera_config(db: Session = Depends(get_db)):
    row = db.query(CameraConfig).filter(CameraConfig.camera_id == settings.camera_id).first()
    if not row:
        return CameraConfigOut(
            camera_id=settings.camera_id,
            camera_name=settings.camera_name,
            site_name=settings.site_name,
            site_address=settings.site_address,
            enabled=settings.camera_enabled,
            rtsp_url_masked=mask_rtsp_url(settings.rtsp_url),
            detection_fps=settings.detection_fps,
            ocr_interval_seconds=settings.ocr_interval_seconds,
            stationary_time_seconds=settings.stationary_time_seconds,
        )
    return _config_out(row)


@router.put("/camera-config", response_model=CameraConfigOut)
def put_camera_config(payload: CameraConfigIn, db: Session = Depends(get_db)):
    row = db.query(CameraConfig).filter(CameraConfig.camera_id == payload.camera_id).first()
    if not row:
        row = CameraConfig(camera_id=payload.camera_id)
        db.add(row)
    row.camera_name = payload.camera_name
    row.site_name = payload.site_name
    row.site_address = payload.site_address
    row.enabled = int(payload.enabled)
    row.roi_json = json.dumps(payload.roi)
    row.entry_line_json = json.dumps(payload.entry_line)
    row.exit_line_json = json.dumps(payload.exit_line)
    row.detection_fps = payload.detection_fps
    row.ocr_interval_seconds = payload.ocr_interval_seconds
    row.stationary_time_seconds = payload.stationary_time_seconds
    row.rtsp_url_masked = mask_rtsp_url(settings.rtsp_url)
    row.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return _config_out(row)


@router.get("/events", response_model=list[TankerEventOut])
def list_events(limit: int = 100, db: Session = Depends(get_db)):
    return db.query(TankerEvent).order_by(TankerEvent.created_at.desc()).limit(limit).all()


@router.post("/exports/excel")
def export_excel(db: Session = Depends(get_db)):
    path = export_events_xlsx(db)
    return FileResponse(path, filename=path.name)


@router.post("/exports/google-sheets")
def sync_google_sheets(db: Session = Depends(get_db)):
    return GoogleSheetsSync().sync(db)


def _config_out(row: CameraConfig) -> CameraConfigOut:
    return CameraConfigOut(
        camera_id=row.camera_id,
        camera_name=row.camera_name,
        site_name=row.site_name,
        site_address=row.site_address,
        enabled=bool(row.enabled),
        rtsp_url_masked=row.rtsp_url_masked,
        roi=json.loads(row.roi_json or "[]"),
        entry_line=json.loads(row.entry_line_json or "[]"),
        exit_line=json.loads(row.exit_line_json or "[]"),
        detection_fps=row.detection_fps,
        ocr_interval_seconds=row.ocr_interval_seconds,
        stationary_time_seconds=row.stationary_time_seconds,
        updated_at=row.updated_at,
    )
