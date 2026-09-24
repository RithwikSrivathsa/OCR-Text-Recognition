import asyncio
from dataclasses import dataclass
from datetime import datetime

import cv2
import structlog

from app.core.config import settings

log = structlog.get_logger()


@dataclass
class CameraHealth:
    connected: bool = False
    last_frame_at: datetime | None = None
    last_error: str = ""


class RtspStreamManager:
    def __init__(self):
        self.health = CameraHealth()
        self._capture = None

    async def frames(self):
        if not settings.camera_enabled:
            log.info("stream.disabled")
            while True:
                await asyncio.sleep(1)
                yield None

        while True:
            try:
                if self._capture is None or not self._capture.isOpened():
                    self._connect()
                ok, frame = self._capture.read()
                if not ok:
                    raise RuntimeError("frame read failed")
                self.health.connected = True
                self.health.last_frame_at = datetime.utcnow()
                yield frame
            except Exception as exc:
                self.health.connected = False
                self.health.last_error = str(exc)
                log.warning("stream.reconnect_scheduled", error=str(exc))
                self._release()
                await asyncio.sleep(settings.reconnect_interval_seconds)

    def _connect(self) -> None:
        if not settings.rtsp_url:
            raise RuntimeError("RTSP_URL is not configured")
        self._capture = cv2.VideoCapture(settings.rtsp_url, cv2.CAP_FFMPEG)
        if not self._capture.isOpened():
            raise RuntimeError("unable to open RTSP stream")
        log.info("stream.connected", camera_id=settings.camera_id)

    def _release(self) -> None:
        if self._capture is not None:
            self._capture.release()
        self._capture = None

    async def stop(self) -> None:
        self._release()

