from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.cache import create_cache
from app.config import CACHE_DEFAULT_TTL, REDIS_URL
from app.database import init_db

STATIC_DIR = Path(__file__).parent / "static"

cache = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global cache
    init_db()
    cache = create_cache(redis_url=REDIS_URL, default_ttl=CACHE_DEFAULT_TTL)
    app.state.cache = cache
    yield
    cache.clear()


app = FastAPI(
    title="AI Automation Hospital AI Agent",
    description=(
        "Standalone AI intelligence layer for AI Automation Hospital. "
        "Scan a curtain barcode and get instant recommendations for "
        "which building, floor, room, and track to install it on."
    ),
    version="0.4.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1", tags=["recommendations"])
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
def root():
    return FileResponse(str(STATIC_DIR / "index.html"))
