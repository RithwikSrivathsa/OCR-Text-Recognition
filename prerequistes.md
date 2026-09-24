# Prerequisites

This project runs best with Docker Compose. You can run everything locally too, but Docker is the recommended path because it installs the backend and frontend dependencies inside containers.

## Required Software

Install these before running the project:

| Tool | Why It Is Needed | Where To Get It |
| --- | --- | --- |
| Docker Desktop | Runs the backend and frontend containers | https://www.docker.com/products/docker-desktop/ |
| Git | Cloning/version control and Git Bash on Windows | https://git-scm.com/downloads |
| PowerShell | Windows command line, already included on Windows | https://learn.microsoft.com/powershell/ |
| Git Bash | Optional terminal included with Git for Windows | https://git-scm.com/downloads |

Optional, only needed if you want to run services without Docker:

| Tool | Why It Is Needed | Where To Get It |
| --- | --- | --- |
| Python 3.11 | Backend runtime outside Docker | https://www.python.org/downloads/ |
| Node.js 22 LTS | Frontend runtime outside Docker | https://nodejs.org/ |
| FFmpeg | RTSP/video decoding outside Docker | https://ffmpeg.org/download.html |

## Hardware And Camera Requirements

- CCTV/IP camera with an RTSP stream.
- RTSP URL, usually similar to:

```text
rtsp://username:password@camera-ip:554/stream
```

- Enough CPU/GPU for the detector and OCR model you later choose.
- Disk space for SQLite database files, Excel exports, and selected snapshot images.

The system does not store full RTSP video by default.

## Backend Python Libraries

The backend dependencies are listed in:

```text
backend/requirements.txt
```

Docker installs them automatically. Main backend libraries:

| Library | Purpose | Package Source |
| --- | --- | --- |
| FastAPI | Backend API framework | https://pypi.org/project/fastapi/ |
| Uvicorn | ASGI server for FastAPI | https://pypi.org/project/uvicorn/ |
| Pydantic Settings | Environment/config management | https://pypi.org/project/pydantic-settings/ |
| SQLAlchemy | Database ORM | https://pypi.org/project/SQLAlchemy/ |
| Alembic | Database migrations | https://pypi.org/project/alembic/ |
| OpenCV headless | RTSP/video/image processing | https://pypi.org/project/opencv-python-headless/ |
| NumPy | Numeric/image array operations | https://pypi.org/project/numpy/ |
| Pandas | Tabular event export handling | https://pypi.org/project/pandas/ |
| openpyxl | Excel `.xlsx` export | https://pypi.org/project/openpyxl/ |
| structlog | Structured backend logging | https://pypi.org/project/structlog/ |
| pytest | Backend tests | https://pypi.org/project/pytest/ |

Install manually only if running without Docker:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Frontend Libraries

The frontend dependencies are listed in:

```text
frontend/package.json
```

Docker installs them automatically. Main frontend libraries:

| Library | Purpose | Package Source |
| --- | --- | --- |
| React | Dashboard UI | https://www.npmjs.com/package/react |
| React DOM | Browser rendering for React | https://www.npmjs.com/package/react-dom |
| Vite | Frontend dev server/build tool | https://www.npmjs.com/package/vite |
| TypeScript | Typed frontend code | https://www.npmjs.com/package/typescript |
| lucide-react | Dashboard icons | https://www.npmjs.com/package/lucide-react |
| Recharts | Charts/statistics support | https://www.npmjs.com/package/recharts |

Install manually only if running without Docker:

```powershell
cd frontend
npm install
npm run dev
```

## ML / OCR Libraries To Add Later

The current project has replaceable adapters for detector, tracker, OCR, and translation. For production accuracy, add licensed models/libraries later.

Recommended options:

| Component | Suggested Library/Model | Where To Get It | Notes |
| --- | --- | --- | --- |
| Object detection | Custom tanker detector or YOLO-compatible model | https://docs.ultralytics.com/ or your own training pipeline | Verify license before commercial/private deployment. |
| Tracking | ByteTrack or BoT-SORT | https://github.com/FoundationVision/ByteTrack / https://github.com/NirAharon/BoT-SORT | Replace `SimpleIoUTracker` with production tracker. |
| Kannada OCR | PaddleOCR | https://github.com/PaddlePaddle/PaddleOCR | Configure Kannada recognition assets. |
| Translation | AI4Bharat IndicTrans2 | https://github.com/AI4Bharat/IndicTrans2 | Run locally; send only validated Kannada text, not images. |
| Google Sheets sync | Google Sheets API | https://developers.google.com/sheets/api | Requires Google Cloud credentials. |

Important: document every model license under:

```text
ml/detection/pretrained/README.md
```

## Environment Setup

Create your local `.env` file from the sample:

### PowerShell

```powershell
copy .env.example .env
```

### Git Bash

```bash
cp .env.example .env
```

Then edit `.env` and set your camera details:

```text
RTSP_URL=rtsp://username:password@camera-ip:554/stream
CAMERA_ID=camera-08
CAMERA_NAME=Camera 08
SITE_NAME=Water Tanker Site
SITE_ADDRESS=Your site address
CAMERA_ENABLED=true
```

If you do not have the camera ready yet, keep:

```text
CAMERA_ENABLED=false
```

## Start With Docker

Run these commands from the project root:

```text
C:\Projects\Neeraj Project
```

### PowerShell

```powershell
cd "C:\Projects\Neeraj Project"
copy .env.example .env
docker compose up --build
```

### Git Bash

```bash
cd "/c/Projects/Neeraj Project"
cp .env.example .env
docker compose up --build
```

After startup:

| Service | URL |
| --- | --- |
| Backend API docs | http://localhost:8000/docs |
| Backend health | http://localhost:8000/health |
| Frontend dashboard | http://localhost:5173 |

## Stop Docker

### PowerShell

```powershell
docker compose down
```

### Git Bash

```bash
docker compose down
```

## Rebuild After Code Changes

Use this when dependencies or Dockerfiles change:

### PowerShell

```powershell
docker compose up --build
```

### Git Bash

```bash
docker compose up --build
```

Use this for a clean rebuild:

### PowerShell

```powershell
docker compose down
docker compose build --no-cache
docker compose up
```

### Git Bash

```bash
docker compose down
docker compose build --no-cache
docker compose up
```

## Run Tests

If Python dependencies are installed locally:

### PowerShell

```powershell
python -m pytest
```

### Git Bash

```bash
python -m pytest
```

Inside Docker, run:

### PowerShell

```powershell
docker compose run --rm backend pytest
```

### Git Bash

```bash
docker compose run --rm backend pytest
```

## Common Problems

### Docker command is not found

Install Docker Desktop and restart your terminal.

### Docker Desktop is not running

Open Docker Desktop first, wait until it says Docker is running, then run:

```powershell
docker compose up --build
```

### Port already in use

The project uses:

- Backend: `8000`
- Frontend: `5173`

Stop the app using that port, or change the ports in `docker-compose.yml`.

### RTSP camera does not connect

Check:

- Camera is powered on.
- The RTSP URL is correct.
- Your computer is on the same network as the camera.
- Username/password are correct.
- Camera RTSP streaming is enabled.
- Firewall allows the connection.

### Frontend opens but shows offline camera

This is expected if:

- `CAMERA_ENABLED=false`
- RTSP URL is missing
- Camera is unreachable
- Backend is still reconnecting

## Recommended First Run

1. Install Docker Desktop.
2. Start Docker Desktop.
3. Open PowerShell.
4. Run:

```powershell
cd "C:\Projects\Neeraj Project"
copy .env.example .env
docker compose up --build
```

5. Open:

```text
http://localhost:5173
```

6. Open API docs:

```text
http://localhost:8000/docs
```

