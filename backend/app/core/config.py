from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "local"
    database_url: str = "sqlite:///./data/tanker_monitor.db"
    snapshot_dir: Path = Path("./data/snapshots")
    export_dir: Path = Path("./data/exports")

    rtsp_url: str = ""
    camera_id: str = "camera-08"
    camera_name: str = "Camera 08"
    site_name: str = "Water Tanker Site"
    site_address: str = ""
    camera_enabled: bool = False

    reconnect_interval_seconds: int = 10
    detection_fps: float = 2.0
    ocr_interval_seconds: int = 300
    stationary_time_seconds: int = 300
    stationary_distance_threshold_pixels: float = 24.0
    detection_confidence_threshold: float = 0.45
    ocr_confidence_threshold: float = 0.60
    track_timeout_seconds: int = 10

    detector_type: str = "generic_truck"
    detector_model_path: str = ""
    translation_provider: str = "offline_stub"

    google_sheets_enabled: bool = False
    google_sheets_spreadsheet_id: str = ""

    default_roi: list[list[int]] = Field(default_factory=list)
    entry_line: list[list[int]] = Field(default_factory=list)
    exit_line: list[list[int]] = Field(default_factory=list)


settings = Settings()

