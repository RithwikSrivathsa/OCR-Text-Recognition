from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


Point = list[int]


class CameraConfigIn(BaseModel):
    camera_id: str
    camera_name: str
    site_name: str
    site_address: str = ""
    enabled: bool = False
    roi: list[Point] = Field(default_factory=list)
    entry_line: list[Point] = Field(default_factory=list)
    exit_line: list[Point] = Field(default_factory=list)
    detection_fps: float = 2.0
    ocr_interval_seconds: int = 300
    stationary_time_seconds: int = 300


class CameraConfigOut(CameraConfigIn):
    rtsp_url_masked: str = ""
    updated_at: datetime | None = None


class HealthOut(BaseModel):
    status: str
    camera_connected: bool
    last_frame_at: datetime | None
    active_tracks: int


class TankerEventOut(BaseModel):
    id: int
    camera_id: str
    site_name: str
    tracker_id: str
    state: str
    entry_time: datetime | None
    exit_time: datetime | None
    duration_seconds: float | None
    text_kn: str
    text_en: str
    ocr_confidence: float | None
    snapshot_path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LiveStatus(BaseModel):
    camera: dict[str, Any]
    active_tankers: list[dict[str, Any]]
    updated_at: datetime

