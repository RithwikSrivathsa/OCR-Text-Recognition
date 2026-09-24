from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class EventState(str, Enum):
    NOT_PRESENT = "NOT_PRESENT"
    ENTERING = "ENTERING"
    PRESENT = "PRESENT"
    EXITING = "EXITING"
    COMPLETED = "COMPLETED"


class CameraConfig(Base):
    __tablename__ = "camera_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    camera_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    camera_name: Mapped[str] = mapped_column(String(255))
    site_name: Mapped[str] = mapped_column(String(255))
    site_address: Mapped[str] = mapped_column(Text, default="")
    enabled: Mapped[int] = mapped_column(Integer, default=0)
    rtsp_url_masked: Mapped[str] = mapped_column(Text, default="")
    roi_json: Mapped[str] = mapped_column(Text, default="[]")
    entry_line_json: Mapped[str] = mapped_column(Text, default="[]")
    exit_line_json: Mapped[str] = mapped_column(Text, default="[]")
    detection_fps: Mapped[float] = mapped_column(Float, default=2.0)
    ocr_interval_seconds: Mapped[int] = mapped_column(Integer, default=300)
    stationary_time_seconds: Mapped[int] = mapped_column(Integer, default=300)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TankerEvent(Base):
    __tablename__ = "tanker_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    camera_id: Mapped[str] = mapped_column(String(128), index=True)
    site_name: Mapped[str] = mapped_column(String(255))
    tracker_id: Mapped[str] = mapped_column(String(128), index=True)
    state: Mapped[str] = mapped_column(String(32), default=EventState.PRESENT.value)
    entry_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    exit_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    text_kn: Mapped[str] = mapped_column(Text, default="")
    text_en: Mapped[str] = mapped_column(Text, default="")
    ocr_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    ocr_polygon_json: Mapped[str] = mapped_column(Text, default="[]")
    tanker_bbox_json: Mapped[str] = mapped_column(Text, default="[]")
    snapshot_path: Mapped[str] = mapped_column(Text, default="")
    preprocessing_method: Mapped[str] = mapped_column(String(128), default="")
    ocr_model_version: Mapped[str] = mapped_column(String(128), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

