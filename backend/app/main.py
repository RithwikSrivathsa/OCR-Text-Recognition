from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.logging import configure_logging
from app.core.runtime import runtime
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    init_db()
    await runtime.start()
    yield
    await runtime.stop()


app = FastAPI(
    title="CCTV Water Tanker Monitoring API",
    version="0.1.0",
    description="RTSP tanker detection, tracking, Kannada OCR, translation, and event export API.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
