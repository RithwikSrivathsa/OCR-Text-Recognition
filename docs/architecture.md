# Architecture

The runtime path is:

RTSP stream -> detector -> tracker -> ROI/event manager -> stationary snapshot policy -> tanker crop/OCR -> translation -> database -> exports/dashboard.

The backend keeps detector, tracker, OCR, and translation behind small contracts. Application state should never depend on a model-specific return shape.

## Replaceable Components

- `BaseVehicleDetector`: maps model detections to `Detection`.
- `SimpleIoUTracker`: placeholder with the same outward contract expected from ByteTrack or BoT-SORT.
- `KannadaOcrProcessor`: target for PaddleOCR Kannada model integration.
- `KannadaTranslator`: target for IndicTrans2 or another local Kannada-English translator.

## Persistence

SQLite is the default local store. Events contain entry/exit times even when no OCR snapshot was captured. Snapshot metadata is attached later when the stationary policy triggers an OCR capture.

## RTSP Safety

RTSP credentials are read from environment variables. API responses only return masked URLs. Full video is not stored.

