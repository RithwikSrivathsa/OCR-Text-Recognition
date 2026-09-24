# CCTV Water Tanker Monitoring System

Production-oriented CCTV analytics scaffold for monitoring water tankers from an RTSP/IP camera.

The system is designed around replaceable model adapters so detector, tracker, OCR, and translation quality can improve without rewriting application logic.

## Features

- FastAPI backend with health checks, OpenAPI docs, REST APIs, and SSE status stream.
- SQLite persistence through SQLAlchemy.
- Robust RTSP stream manager with reconnect state and no full-video storage.
- Separate lightweight detection/tracking loop from expensive OCR snapshots.
- Configurable camera, site, ROI, entry/exit lines, processing FPS, and OCR interval.
- Event state machine for entry, presence, exit, and completion.
- Stationary tanker snapshot logic with configurable 5-minute default interval.
- Kannada OCR service abstraction with preprocessing metadata and OCR polygons.
- Kannada to English translation service abstraction.
- Annotated snapshot storage.
- Excel export and Google Sheets sync extension point.
- React/TypeScript/Vite dashboard.
- Docker and Docker Compose.
- ML folder structure for custom tanker detector training.

## Quick Start

```powershell
copy .env.example .env
docker compose up --build
```

Backend API: http://localhost:8000/docs

Frontend dashboard: http://localhost:5173

## Model And License Notes

The detector interface is intentionally generic. The included `GenericTruckDetector` is an adapter placeholder for a deployable detector and can be replaced by `CustomTankerDetector`.

If you choose an Ultralytics YOLO model or library for private/commercial deployment, verify the applicable Ultralytics license before shipping. Do not assume AGPL components are suitable for proprietary commercial use. Keep model license records under `ml/detection/pretrained/README.md` or alongside exported weights.

## Important Runtime Behavior

- Entry and exit events are independent from OCR.
- OCR is not run on every frame.
- Complete RTSP video is not stored.
- Only snapshots required for analysis are saved.
- RTSP credentials must remain in environment variables or Docker secrets.

## Project Layout

```text
backend/        FastAPI app, CV pipeline, database, exports
frontend/       React dashboard
ml/detection/   detector data/training/checkpoint/export structure
data/           local SQLite database, snapshots, exports
docs/           architecture and API notes
```

